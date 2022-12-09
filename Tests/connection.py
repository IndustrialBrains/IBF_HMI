"""Provide a PyADS connection to a PLC"""
from time import sleep, time
from typing import Any

import pyads

# conn = pyads.Connection("127.0.0.1.1.1", pyads.PORT_TC3PLC1)
# conn = pyads.Connection("192.168.178.25.1.1", pyads.PORT_TC3PLC1)
# conn = pyads.Connection("PC-975086", pyads.PORT_TC3PLC1)
conn = pyads.Connection("41.151.80.134.1.1", pyads.PORT_TC3PLC1)

ADS_COMMAND_DELAY = 0.020  # (sec) time to allow the PLC to handle ADS commands
PLC_CYCLETIME = 0.010  # (sec)


class TimeOutError(Exception):  # pylint: disable=missing-class-docstring
    ...


def cold_reset(timeout: float = 1.0) -> None:
    """Cold reset the PLC (similar to clicking the `Reset cold` button)
    NOTE: A cold reset deactivates all debug breakpoints in the PLC."""
    conn.write_control(pyads.ADSSTATE_RESET, 0, 0, pyads.PLCTYPE_BOOL)
    conn.write_control(pyads.ADSSTATE_RUN, 0, 0, pyads.PLCTYPE_BOOL)

    start_time = time()
    while (time() - start_time) < timeout:
        (ads_state, _) = conn.read_state()
        if ads_state == pyads.ADSSTATE_RUN:
            return
        sleep(ADS_COMMAND_DELAY)

    raise TimeOutError(f"Cold reset failed (timeout after {timeout} seconds)")


def wait_cycles(cycles: int) -> None:
    """Wait for a number of PLC cycles (roughly). Cycletime is a fixed value: `PLC_CYCLETIME`
    Note that this will not match the exact number of cycles: the Python process
    is not running in sync with the PLC and no exact timers are used."""
    sleep(PLC_CYCLETIME * cycles)


def wait_value(var: str, value: Any, timeout: float) -> bool:
    """Wait for a variable to get a value. Return True on success, False on timeout."""
    start_time = time()
    while (time() - start_time) < timeout:
        if conn.read_by_name(var) == value:
            return True
        wait_cycles(1)
    return False


def trigger_falling_edge(var: str) -> None:
    """Trigger a falling edge"""
    conn.write_by_name(var, True)
    wait_cycles(1)
    conn.write_by_name(var, False)
    wait_cycles(1)


def trigger_rising_edge(var: str) -> None:
    """Trigger a rising edge"""
    conn.write_by_name(var, False)
    wait_cycles(1)
    conn.write_by_name(var, True)
    wait_cycles(1)
