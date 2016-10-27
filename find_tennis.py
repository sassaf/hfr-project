import cv2
import numpy
#import settings
import color_editing

camera = cv2.VideoCapture(0);

#desired_settings = {'width': 640.0, 'saturation': 32.0, 'gain': 128.0, 'brightness': 128.0, 'hue': 13.0,
#                    'contrast': 32.0, 'height': 480.0, 'focus': 0.0}

#new_values = settings.set_settings({}, reset_defaults=False, print_values=False)
#
colors_list = ['green']

ret, frame = camera.read()

while (ret):
    ret, frame = camera.read()
    blurred_frame = cv2.GaussianBlur(frame, (9, 9), 0)
    img_gray = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

    color_frames = color_editing.setting_colors(blurred_frame, colors_list)

    for name in color_frames:
        color_mask = color_frames[name] # color mask is black image with white portions showing where [name] color is

        filtered_frame = cv2.bitwise_and(frame, frame, mask=color_mask) # now only [name] color portions of screen will show, in its color

        name = name[0].upper() + name[1:len(name)]
        cv2.imshow("{} Filtered Frame".format(name), filtered_frame)

    cv2.imshow('Full Color Image', frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q'):
        ret = False
        cv2.destroyAllWindows()

camera.release()
