*evdev* documentation
========================================

:mod:`evdev` provides bindings to the generic input event interface in
Linux.  The *evdev* interface serves the purpose of passing events
generated in the kernel directly to userspace through character
devices that are typically located in ``/dev/input/``.

:mod:`evdev` also comes with bindings to ``uinput``, the userspace
input subsystem. ``Uinput`` allows userspace programs to create and
handle input devices from which input events can be directly injected
into the input subsystem.


Tutorial
--------

Listing accessible event devices::

    >>> from evdev import InputDevice, list_devices

    >>> devices = map(InputDevice, list_devices())

    >>> for dev in devices:
    ...    print( '%-20s %-32s %s' % (dev.fn, dev.name, dev.phys) )
    /dev/input/event1    Dell Dell USB Keyboard           usb-0000:00:12.1-2/input0
    /dev/input/event0    Dell Premium USB Optical Mouse   usb-0000:00:12.0-2/input0

Listing device capabilities::

    >>> dev = InputDevice('/dev/input/event0')

    >>> print(dev)
    device /dev/input/event0, name "Dell Premium USB Optical Mouse", phys "usb-0000:00:12.0-2/input0"

    >>> dev.capabilities()
    ... { 0: [0, 1, 2], 1: [272, 273, 274, 275], 2: [0, 1, 6, 8], 4: [4] }

    >>> dev.capabilities(verbose=True)
    ... { ('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('SYN_MT_REPORT', 2)],
    ...   ('EV_KEY', 1): [('BTN_MOUSE', 272), ('BTN_RIGHT', 273), ('BTN_MIDDLE', 274), ('BTN_SIDE', 275)], ...

Listing device capabilities for devices with absolute axes::

    >>> dev = InputDevice('/dev/input/event7')

    >>> print(dev)
    device /dev/input/event7, name "Wacom Bamboo 2FG 4x5 Finger", phys ""

    >>> dev.capabilities()
    ... { 1: [272, 273, 277, 278, 325, 330, 333] ,
    ...   3: [(0, AbsInfo(min=0, max=15360, fuzz=128, flat=0)),
    ...       (1, AbsInfo(min=0, max=10240, fuzz=128, flat=0))] }

    >>> dev.capabilities(verbose=True)
    ... { ('EV_KEY', 1): [('BTN_MOUSE', 272), ('BTN_RIGHT', 273), ...],
    ...   ('EV_ABS', 3): [(('ABS_X', 0), AbsInfo(min=0, max=15360, fuzz=128, flat=0)),
    ...                   (('ABS_Y', 1), AbsInfo(min=0, max=10240, fuzz=128, flat=0)),] }

    >>> dev.capabilities(absinfo=False)
    ... { 1: [272, 273, 277, 278, 325, 330, 333],
    ...   3: [0, 1, 47, 53, 54, 57] }

Accessing input subsystem constants::

    >>> from evdev import ecodes
    >>> ecodes.KEY_A, ecodes.ecodes['KEY_A']
    ... (30, 30)
    >>> ecodes.KEY[30]
    ... 'KEY_A'
    >>> ecodes.bytype[ecodes.EV_KEY][30]
    ... 'KEY_A'

Reading events::

    >>> from evdev import InputDevice, categorize, ecodes
    >>> dev = InputDevice('/dev/input/event1')

    >>> print(dev)
    device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"

    >>> for event in dev.read_loop():
    ...     if event.type == ecodes.EV_KEY:
    ...         print(categorize(event)) 
    ... # pressing 'a' and holding 'space'
    key event at 1337016188.396030, 30 (KEY_A), down
    key event at 1337016188.492033, 30 (KEY_A), up
    key event at 1337016189.772129, 57 (KEY_SPACE), down
    key event at 1337016190.275396, 57 (KEY_SPACE), hold
    key event at 1337016190.284160, 57 (KEY_SPACE), up

Reading events from multiple devices::

    >>> from evdev import InputDevice
    >>> from select import select

    >>> devices = map(InputDevice, ('/dev/input/event1', '/dev/input/event2'))
    >>> devices = {dev.fd : dev for dev in devices}

    >>> for dev in devices.values(): print(dev)
    device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"
    device /dev/input/event2, name "Logitech USB Laser Mouse", phys "usb-0000:00:12.0-2/input0"

    >>> while True:
    ...    r,w,x = select(devices, [], [])
    ...    for fd in r:
    ...        for event in devices[fd].read():
    ...            print(event)
    event at 1351116708.002230, code 01, type 02, val 01
    event at 1351116708.002234, code 00, type 00, val 00
    event at 1351116708.782231, code 04, type 04, val 458782
    event at 1351116708.782237, code 02, type 01, val 01

Reading events with asyncore::

    >>> from asyncore import file_dispatcher, loop
    >>> from evdev import InputDevice, categorize, ecodes
    >>> dev = InputDevice('/dev/input/event1')

    >>> class InputDeviceDispatcher(file_dispatcher):
    ...     def __init__(self, device):
    ...         self.device = device
    ...         file_dispatcher.__init__(self, device)
    ...
    ...     def recv(self, ign=None):
    ...         return self.device.read()
    ...
    ...     def handle_read(self):
    ...         for event in self.recv():
    ...             print(repr(event))

    >>> InputDeviceDispatcher(dev)
    >>> loop()
    InputEvent(1337255905L, 358854L, 1, 30, 0L)
    InputEvent(1337255905L, 358857L, 0, 0, 0L)

Getting exclusive access to a device::

    >>> dev.grab()  # become the sole recipient of all incoming input events
    >>> dev.ungrab()

Associating classes with event types (see :mod:`events <evdev.events>`)::

    >>> from evdev import categorize, event_factory, ecodes

    >>> class SynEvent(object):
    ...     def __init__(self, event):
    ...         ...

    >>> event_factory[ecodes.EV_SYN] = SynEvent

Injecting events::

    >>> from evdev import UInput, ecodes as e

    >>> ui = UInput()

    >>> # accepts only KEY_* events by default
    >>> ui.write(e.EV_KEY, e.KEY_A, 1)  # KEY_A down
    >>> ui.write(e.EV_KEY, e.KEY_A, 0)  # KEY_A up
    >>> ui.syn()

    >>> ui.close()

Injecting events (2)::

    >>> ev = InputEvent(1334414993, 274296, ecodes.EV_KEY, ecodes.KEY_A, 1)
    >>> with UInput() as ui:
    ...    ui.write_event(ev)
    ...    ui.syn()

Specifying uinput device options::

    >>> from evdev import UInput, AbsInfo, ecodes as e

    >>> cap = {
    ...     e.EV_KEY : [e.KEY_A, e.KEY_B],
    ...     e.EV_ABS : [
    ...         (e.ABS_X, AbsInfo(min=0, max=255, fuzz=0, flat=0)),
    ...         (e.ABS_Y, AbsInfo(0, 255, 0, 0)),
    ...         (e.ABS_MT_POSITION_X, (0, 255, 128, 0)) ]
    ... }

    >>> ui = UInput(cap, name='example-device', version=0x3)
    >>> print(ui)
    name "example-device", bus "BUS_USB", vendor "0001", product "0001", version "0003"
    event types: EV_KEY EV_ABS EV_SYN

    >>> print(ui.capabilities())
    ... { 0: [0, 1, 3], 1: [30, 48],
    ...   3: [(0,  AbsInfo(min=0, max=255, fuzz=0, flat=0)),
    ...       (1,  AbsInfo(min=0, max=255, fuzz=0, flat=0)),
    ...       (53, AbsInfo(min=0, max=255, fuzz=128, flat=0))] }

    >>> # move mouse cursor
    >>> ui.write(e.EV_ABS, e.ABS_X, 20)
    >>> ui.write(e.EV_ABS, e.ABS_Y, 20)
    >>> ui.syn()

Requirements
------------

:mod:`evdev` contains C extension modules and requires the Python development
headers as well as the kernel headers.

On a Debian compatible OS:

.. code-block:: bash

    $ apt-get install python-dev
    $ apt-get install linux-headers-$(uname -r)

On a Redhat compatible OS:

.. code-block:: bash

    $ yum install python-devel
    $ yum install kernel-headers-$(uname -r)

:mod:`evdev` itself requires CPython **>= 2.7**


Installation
------------

Assuming all requirements have been met, the latest stable version of
:mod:`evdev` can be installed from PyPi_, while the development version can be
installed from github_:

.. code-block:: bash

    $ pip install evdev  # latest stable version
    $ pip install git+git://github.com/gvalkov/python-evdev.git # latest development version

Alternatively, :mod:`evdev` can be installed like any other
:mod:`distutils`/:mod:`setuptools`/:mod:`packaging` package:

.. code-block:: bash

    $ git clone github.com/gvalkov/python-evdev.git
    $ cd python-evdev
    $ git checkout $versiontag
    $ python setup.py install



Module Contents
---------------

.. toctree::
   :maxdepth: 2

   moduledoc


Similar Projects
----------------

* `python-uinput`_
* `ruby-evdev`_
* `evdev`_ (ctypes)


License
-------

:mod:`evdev` is released under the terms of the `New BSD License`_.


Todo
----

* Use libudev to find the uinput device node as well as the other input
  devices. Their locations are currently assumed to be ``/dev/uinput`` and
  ``/dev/input/*``.

* More tests.

* Better uinput support (setting device capabilities as in `python-uinput`_)

* Expose more input subsystem functionality (``EVIOCSKEYCODE``, ``EVIOCGREP`` etc)

* Figure out if using ``linux/input.h`` and other kernel headers in your
  userspace program binds it to the GPL2.


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _`New BSD License`: https://raw.github.com/gvalkov/python-evdev/master/LICENSE
.. _PyPi:              http://pypi.python.org/pypi/evdev
.. _github:            https://github.com/gvalkov/python-evdev
.. _python-uinput:     https://github.com/tuomasjjrasanen/python-uinput
.. _ruby-evdev:        http://technofetish.net/repos/buffaloplay/ruby_evdev/doc/
.. _evdev:             http://svn.navi.cx/misc/trunk/python/evdev/
