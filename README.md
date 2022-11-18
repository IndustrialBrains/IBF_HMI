[![GitIgnore](../../actions/workflows/GitIgnore.yml/badge.svg)](../../actions/workflows/GitIgnore.yml)

# Industrial Brainframe - HMI library

## User management
The HMI library contains the default Beckhoff user management settings. Passwords are identical to the user names.

## Testing
This library does not have any automatic tests because there is no test framework available for Beckhoff HMI testing.\
However, a test visualization is available (see `VISU_TEST`), with which you can test parameter screens, manual controls, etc. by hand.

`PRG_TEST` contains the bare minimum code to make the screens fully functional.

## TODO


### Improvements

1. Add Github action (build)
1. Fix errors generated when static analysis rule "Unused variables" is enabled
1. `ManualControl`: 
	- list sometimes contains 1 empty item
1. Remove customer logos, should reside in customer projects





