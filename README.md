[![GitIgnore](../../actions/workflows/GitIgnore.yml/badge.svg)](../../actions/workflows/GitIgnore.yml)

# Industrial Brainframe - HMI library

## User management
The HMI library contains the default Beckhoff user management settings. Passwords are identical to the user names.

## Testing
This library does not have any automatic tests because there is no test framework available for Beckhoff HMI testing.\
However, a test visualization is available (see `VISU_TEST`), with which you can test parameter screens, manual controls, etc. by hand.

`PRG_TEST` contains the bare minimum code to make the screens fully functional.

## TODO

### Must have

1. Create separate PNG based screens for Windows CE (first, check https://infosys.beckhoff.com/content/1033/tc3_plc_intro/136113291.html section about SVG files)

### Should have


### Nice to have
1. Resize parameter/manual screens (make fixed size)
1. `FB_LogView`:
	- do not show zero in alarm icon, only if > 0
	- do not blink button when no fault is active
	- Increase string length of history log Message column

### Improvements

1. Add Github action (build)
1. Remove customer icons, should reside in customer projects





