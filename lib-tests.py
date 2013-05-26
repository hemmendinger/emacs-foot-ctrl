from evdev import InputDevice, categorize, ecodes, list_devices

def list_all():
    '''list all input devices available'''
    devices = map(InputDevice, list_devices())
    for dev in devices:
        print( '%-20s %-32s %s' % (dev.fn, dev.name, dev.phys) )

def live_monitor(eventdev):
    '''monitor all keypresses from device live'''
    dev = InputDevice('/dev/input/' + eventdev)
    print(dev)
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            print(categorize(event))

