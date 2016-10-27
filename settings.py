import cv2
import numpy


camera = cv2.VideoCapture(0)

# Testing possible settings values for camera, most will not work (return -1) but this is how I found value for focus
# for x in range(0, 50):
#     print("{}: {}".format(x, camera.get(x)))

settings_id = {}

## Setting the id's for the various settings
settings_id.update({'timestamp': cv2.CAP_PROP_POS_MSEC})
settings_id.update({'width': cv2.CAP_PROP_FRAME_WIDTH})
settings_id.update({'height': cv2.CAP_PROP_FRAME_HEIGHT})
settings_id.update({'fps': cv2.CAP_PROP_FPS})
settings_id.update({'brightness': cv2.CAP_PROP_BRIGHTNESS})
settings_id.update({'contrast': cv2.CAP_PROP_CONTRAST})
settings_id.update({'saturation': cv2.CAP_PROP_SATURATION})
settings_id.update({'hue': cv2.CAP_PROP_HUE})
settings_id.update({'gain': cv2.CAP_PROP_GAIN})
settings_id.update({'exposure': cv2.CAP_PROP_EXPOSURE})
settings_id.update({'focus': 28}) # hard coded number, not pre-assigned variable like other settings


def set_settings(new_values, reset_defaults, print_values):

    """

    :dict new_values: Name and numerical value for desired value for that setting. If empty, nothing is changed.
    :bool reset_defaults: Resets camera values to pre-determined defaults.
    :bool print_values: Print values of camera settings after changes.
    :return:
    :tuple: Returns the values that were successfully set, failures are shown as their unchanged values.
    """

    ## If requested, set values to defaults for various values from camera
    if (reset_defaults):
        camera.set(settings_id['width'], 640.0)
        camera.set(settings_id['height'], 480.0)
        camera.set(settings_id['fps'], 0.0) # Don't ask me why it's 0.0
        camera.set(settings_id['brightness'], 128.0)
        camera.set(settings_id['contrast'], 32.0)
        camera.set(settings_id['saturation'], 32.0)
        camera.set(settings_id['hue'], 13.0)
        camera.set(settings_id['gain'], 128.0)
        camera.set(settings_id['focus'], 65)
        camera.set(settings_id['exposure'], -5.0)

    # Loop through values in new_values to change, it will only change what's in new_values
    for name in new_values:
        camera.set(settings_id[name], new_values[name])

    # If I get the 60/120 FPS PS3 camera the FPS function will be fun to play around with
    # camera.set(settings_id['fps'], 60.0)

    settings_value = {}
    # Getting various values from camera
    for name in settings_id:
        settings_value.update({name: camera.get(settings_id[name])})

    if print_values:
        print settings_value

    return settings_value
