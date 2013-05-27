# planning from scratch (in progress/incomplete)
#
# someday/maybe:
#   allow user to choose from multiple connected devices or quit
#

imports

DEVICE_CONSTANT	

## initialization
get_device()
monitor_device_events()
behavior_callbacks()

def get_device():
    list_devices()
    match_device()
    grab_device()

    def list_devices():
    	access_usb()
	get_device_list_with_descriptions()
	return list

    def match_device(list):
	find_in_list(DEVICE_CONSTANT)
	check_for_multiple_or_none()
    	warn_and_terminate_if_none() #instruct to connect the device
	warn_and_terminate_if_multiple() #instruct to try with one device
 	return match

    def grab_device(match):
    	#might need to move or launch into loop from here
    	try_getting_device()
	return device

def monitor_device_events():

def behavior_callbacks():

## termination: triggered by CTRL-C
clean_up()

def clean_up():
    close any connections/release any devices
