import usb.core, usb.util
import sys
from evdev import InputDevice, categorize, ecodes, list_devices

def evdev_list_all():
    '''evdev: list all input devices available'''
    devices = map(InputDevice, list_devices())
    for dev in devices:
        print( '%-20s %-32s %s' % (dev.fn, dev.name, dev.phys) )

def evdev_live_monitor(eventdev):
    '''evdev: monitor all keypresses from device live'''
    dev = InputDevice('/dev/input/' + eventdev)
    print(dev)
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            print(categorize(event))

def pyusb_find_all():
    '''pyusb: list device objects, doesn't require elevated permissions'''
    dev = usb.core.find(find_all=True)
    if dev is None:
        print('no devices found')
        return
    for device in dev:
        print(device)
