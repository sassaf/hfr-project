import cv2
import numpy

lower_blue = numpy.array([82, 100, 50])
upper_blue = numpy.array([135, 255, 255])
lower_green = numpy.array([43, 100, 50])
upper_green = numpy.array([82, 255, 255])
lower_purple = numpy.array([135, 100, 50])
upper_purple = numpy.array([165, 255, 255])
lower_red1 = numpy.array([165, 100, 50])
upper_red1 = numpy.array([180, 255, 255])
lower_red2 = numpy.array([0, 100, 50])
upper_red2 = numpy.array([5, 255, 255])
lower_orange = numpy.array([5, 100, 50])
upper_orange = numpy.array([20, 255, 255])
lower_yellow = numpy.array([20, 100, 50])
upper_yellow = numpy.array([43, 255, 255])


def setting_colors(frame, colors_list):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color_frames = {}

    if 'blue' in colors_list:

        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        #blue_image = cv2.bitwise_and(frame, frame, mask=blue_mask)
        color_frames.update({'blue': blue_mask})

    if 'green' in colors_list:

        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        #green_image = cv2.bitwise_and(frame, frame, mask=green_mask)
        color_frames.update({'green': green_mask})

    if 'purple' in colors_list:

        purple_mask = cv2.inRange(hsv, lower_purple, upper_purple)
        #purple_image = cv2.bitwise_and(frame, frame, mask=purple_mask)
        color_frames.update({'purple': purple_mask})

    if 'red' in colors_list:
        red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        #red_image = cv2.bitwise_and(frame, frame, mask=red_mask)
        color_frames.update({'red': red_mask})

    if 'orange' in colors_list:

        orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
        #orange_image = cv2.bitwise_and(frame, frame, mask=orange_mask)
        color_frames.update({'orange': orange_mask})

    if 'yellow' in colors_list:

        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        #yellow_image = cv2.bitwise_and(frame, frame, mask=yellow_mask)
        color_frames.update({'yellow': yellow_mask})

    return color_frames
