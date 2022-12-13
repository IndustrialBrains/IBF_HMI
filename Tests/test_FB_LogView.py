"""Tests for visu LogView
NOTE: This is a convenience script for manual tests."""
# pylint: disable=missing-function-docstring, missing-class-docstring, invalid-name
import sys
import unittest
from enum import IntEnum, auto

import pyads

from connection import cold_reset, conn, wait_value

COLD_RESET = True


class E_FaultTypes(IntEnum):
    OM = 0  # Operator message
    MC = auto()  # Missing condition
    CF = auto()  # Cycle Fault
    FF = auto()  # Fatal fault
    OW = auto()  # Operator warning


class Tests(unittest.TestCase):

    PREFIX = "PRG_TEST_LOGVIEW"

    @classmethod
    def setUpClass(cls) -> None:
        conn.open()
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        conn.close()

    def setUp(self) -> None:
        if COLD_RESET:
            cold_reset()
        conn.write_by_name(f"{self.PREFIX}.bEnableTests", True)
        # Disable automatic clearing of faults during test
        conn.write_by_name("GVL_Utilities.fbFaultHandler.nMaxInactiveCycles", 0)
        return super().setUp()

    def _update_fault(
        self,
        faulttype: E_FaultTypes,
        description: str | None = None,
        active: bool = True,
    ):
        """(De)activate a fault by writing data to stFault"""
        # Pause execution to make sure the whole FaultType struct is written before it gets handled.
        # TODO: use conn.write_structure_by_name
        conn.write_by_name(f"{self.PREFIX}.bEnableTests", False)
        conn.write_by_name(
            f"{self.PREFIX}.fbBase.stFault.FaultType", faulttype, pyads.PLCTYPE_UINT
        )
        if description:
            conn.write_by_name(f"{self.PREFIX}.fbBase.stFault.description", description)
        conn.write_by_name(f"{self.PREFIX}.fbBase.stFault.Active", active)
        conn.write_by_name(f"{self.PREFIX}.bEnableTests", True)

    def _trigger_reset(self):
        """Trigger CmdReset"""
        conn.write_by_name(f"{self.PREFIX}.bCmdReset", True)
        self.assertEqual(
            wait_value(
                f"{self.PREFIX}.bCmdReset",
                False,
                0.5,
            ),
            True,
        )

    def test_add_fault(self):
        """Add a fault of each type, and reset the last one added"""
        # active_faults = 0
        for faulttype in E_FaultTypes:
            self._update_fault(faulttype, str(faulttype))

        conn.write_by_name(f"{self.PREFIX}.fbBase.stFault.Active", False)
        self._trigger_reset()


if __name__ == "__main__":
    for _ in range(1):  # increase value to repeat the test
        test = unittest.main(verbosity=2, exit=False, failfast=True)
        if not test.result.wasSuccessful():
            sys.exit(-1)
