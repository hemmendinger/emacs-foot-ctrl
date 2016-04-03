emacs-foot-ctrl
===============

Adapting a foot switch to simulate CTRL when released for improved ergonomics.

I believe that it is best if the foot were to always rest on the pedal.
If a user has to hold their foot above the pedal without pressing it,
it results in unnecessary strain, especially if most of the time you are not
going to be pushing CTRL. 

So it is likely best if the neutral position was when the pedal is pressed,
and the active position is a release. Or it's just my personal preference.

I've found the quality of this food pedal is not very satisfying for long periods of use, and works better attached to a board or another surface to keep it anchored.


## Credits

Borrowing from and inspired by:
https://github.com/ktemkin/software-vim-clutch

Which was inspired by:
https://github.com/alevchuk/vim-clutch#readme


## How to Setup

1. Connect foot switch

2. Configure the foot switch to use one of the following:
    Alt, Ctrl, Shift, Win/Super

3. Ensure the python-evdev library is installed

4. Run the emacs-clutch.py with permissions to access the hardware

Terminate the program:

  Ctrl-C


## Hardware Setup: hardware_device_tests.py

Some might find this extra file helpful for configuring or testing to see if
a pedal is correctly configured.


## Support and Dependencies

This was only tested on Ubuntu Linux. Let me know if it needs adjustments for another flavor.

Requires:
Python2
evdev
