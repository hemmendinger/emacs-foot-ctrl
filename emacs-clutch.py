#!/usr/bin/env python2.7

import asyncore
import evdev
import signal
import logging, time

## notes
# looks like handlers have unused parameters

#hack to keep asyncore from hogging 100% cpu
#time.sleep(TIME_SLEEP) added to asyncore loop
#0.02 keeps it consistently below 1
TIME_SLEEP = 0.02

#Stores the product names for each device which can be used as a emacs-clutch. 
COMPATIBLE_NAMES = ["RDing FootSwitchV1.1"]

#
# Advanced "configuration"
#

def press_handler(output_device, input_device, event):
    """
        Pedal-press handler.
        This function is called whenever the clutch-pedal is pushed.
    """
#    send_keypress(output_device, 'KEY_ESC')
#    send_keypress(output_device, 'KEY_I')

#    send_keyrelease(output_device, 'KEY_I')
    send_keyrelease(output_device, 'KEY_CAPSLOCK')



def release_handler(output_device, input_device, event):
    """
        Pedal-release handler.
        This function is called whenever the clutch-pedal is released.
    """
    #send_keypress(output_device, 'KEY_I')
    send_keypress(output_device, 'KEY_CAPSLOCK')


#
# Core code starts here; modify the text below only if you know what you're doing!
#

class ClutchEventDispatcher(asyncore.file_dispatcher):
    """
        Special event handler designed to process asynchronous input
        from a emacs-clutch footpedal.
    """

    def __init__(self, device, press_handler, release_handler):
        """
            Initializes a new ClutchEventDispatcher, setting up a "listener" for
            foot-pedal events.
        """

        #Store an internal reference to the foot-pedal device.
        self.device = device

        #And store references to the press and release callbacks.
        self.press_handler = press_handler
        self.release_handler = release_handler

        #And request that asyncore listend for changes in the event "file".
        asyncore.file_dispatcher.__init__(self, device)


    def recv(self, ign=None):
        """
            Overloaded function which recieves events from the foot-pedal.
            Used by asyncore to check for asynchronous input events.
        """
        return self.device.read()


    def handle_read_old(self):
        """
            Event handler for a foot-pedal event.
        """

        #Handle each of the received events, in the order that they were received.
        for event in self.recv():
#            print(event)
            if event.type == evdev.ecodes.EV_KEY:
                # default event.type = 1
                #Wrap the event in the appropriate class...
                event = evdev.categorize(event)
#                print(event)

                #If the clutch has been depressed, call the press handler.
                if event.keystate == event.key_down:
                    self.press_handler(self.device, event)

                #Otherwise, call the release handler.
                elif event.keystate == event.key_up:
                    self.release_handler(self.device, event)


    def handle_read(self):
        """
            Event handler for a foot-pedal event.
        """
        #Handle each of the received events, in the order that they were received.
        for event in self.recv():
#            print(event)
            if event.type == evdev.ecodes.EV_KEY:
                # default event.type = 1
                #Wrap the event in the appropriate class...
                event = evdev.categorize(event)


                #If the clutch has been depressed, call the press handler.
                if event.keystate == event.key_down:
                    self.press_handler(self.device, event)

                #Otherwise, call the release handler.
                elif event.keystate == event.key_up:
                    self.release_handler(self.device, event)



def main():
    """
        Handles events for all keyboard devices.
    """

    #Create a virtual keyboard device, which will be used to _send_ the resultant key-presses.
    output_device = evdev.UInput(events=None, name='Emacs-Clutch Foot-Pedal')

    #And get a list of all foot-pedal devices which should be monitored for events.
    input_devices = compatible_devices()

    #Create generic press and release handlers which are closed over the output device.
    press_callback = lambda input_device, event : press_handler(output_device, input_device, event)
    release_callback = lambda input_device, event : release_handler(output_device, input_device, event)

    #For each foot-pedal detected.
    #TODO: review if it matters that it is looking for more than one device to
    #      grab, when [usually] we will only want to use 1 pedal;
    #      and if we have more than one pedal, we may not want that pedal
    #      to be grabbed by this program; should warn user at least if
    #      more than one device and ask to proceed and recommend unplugging
    #      any unused device that shouldn't be grabbed
    for device in input_devices:

        #Attain sole ownership of the device, so its events don't populate back up to X.
        device.grab()

        #And register handlers for the device's events.
        ClutchEventDispatcher(device, press_callback, release_callback)

    #Add a handler which releases devices on SIGTERM.
    signal.signal(signal.SIGTERM, lambda : cleanup(output_device, input_devices))

    #And loop indefinitely, handling "asynchronous" press events.
    try:
        while True:
            time.sleep(TIME_SLEEP)
            asyncore.loop(count=1)

    #Allow the program to be closed by CTRL+C.
    except KeyboardInterrupt:
        cleanup(output_device, input_devices)
        print('\ncleanup on CTRL-C complete')


def compatible_devices():
    """
        Returns a list of compatible evdev devices.
    """

    #Get reference to each evdev device installed in the system.
    devices = [evdev.InputDevice(d) for d in evdev.list_devices()]

    #Filter the device list so it only includes clutch-compatible foot switches.
    return [d for d in devices if d.name in COMPATIBLE_NAMES]



def send_keypress(output_device, keycode):
    """
        Sends a key-down and key-up event in rapid succession.
    """

    #Send a key-down event, followed by a key-up event.
    output_device.write(evdev.ecodes.EV_KEY, evdev.ecodes.ecodes[keycode], 1)
#    output_device.write(evdev.ecodes.EV_KEY, evdev.ecodes.ecodes[keycode], 0)

    #And send a synchronization signal
    output_device.syn()

def send_keyrelease(output_device, keycode):
    """
       Send on key release, when the pedal is in a released/neutral position
    """
    # send key-up
    output_device.write(evdev.ecodes.EV_KEY, evdev.ecodes.ecodes[keycode], 0)
    #And send a synchronization signal
    output_device.syn()

def cleanup(output_device, input_devices):
    """
        Cleans up all device ownerships on program close.
    """

    #Release each of the input devices...
    for device in input_devices:
        device.ungrab()

    #And close the virtual output device.
    output_device.close()




main()
