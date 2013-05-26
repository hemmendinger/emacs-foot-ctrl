emacs-foot-ctrl
===============

Adapting a foot switch to simulate CTRL when released for improved ergonomics.

I believe that it is best if the foot were to always rest on the pedal.
If a user has to hold their foot above the pedal without pressing it,
it results in unnecessary strain, especially if most of the time you are not
going to be pushing CTRL. 

So it is likely best if the neutral position was when the pedal is pressed,
and the active position is a release. Or it's just my personal preference.

(Only tested on Ubuntu. Let me know if it needs adjustments for another flavor.)

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

Ctrl-C to terminate the program
