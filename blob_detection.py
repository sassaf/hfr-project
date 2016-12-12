import cv2
import numpy as np

def nothing(x):
    pass

#cv2.namedWindow('Value Control')

#cv2.createTrackbar('Min Area', 'Value Control', 1000, 50000, nothing)
#cv2.createTrackbar('Max Area', 'Value Control', 70000, 100000, nothing)
#cv2.createTrackbar('Min Blue', 'Value Control', 82, 180, nothing)
#cv2.createTrackbar('Max Blue', 'Value Control', 135, 180, nothing)
#cv2.createTrackbar('Min Circularity', 'Value Control', 75, 100, nothing)
#cv2.createTrackbar('Min Threshold', 'Value Control',180, 255, nothing)
#cv2.createTrackbar('Max Threshold', 'Value Control',200, 255, nothing)
#cv2.createTrackbar('Min Saturation', 'Value Control',100, 255, nothing)
#cv2.createTrackbar('Max Saturation', 'Value Control',255, 255, nothing)
#cv2.createTrackbar('Min Value', 'Value Control',50, 255, nothing)
#cv2.createTrackbar('Max Value', 'Value Control',255, 255, nothing)

def find(frame):

    # Trackbar Values
    #minBlue = cv2.getTrackbarPos('Min Blue', 'Value Control')
    #maxBlue = cv2.getTrackbarPos('Max Blue', 'Value Control')
    #params.minCircularity = cv2.getTrackbarPos('Min Circularity', 'Value Control')/100.0
    #params.minThreshold = cv2.getTrackbarPos('Min Threshold', 'Value Control')
    #params.maxThreshold = cv2.getTrackbarPos('Max Threshold', 'Value Control')
    #params.minArea = cv2.getTrackbarPos('Min Area', 'Value Control')
    #params.maxArea = cv2.getTrackbarPos('Max Area', 'Value Control')
    #low_sat = cv2.getTrackbarPos('Min Saturation', 'Value Control')
    #high_sat = cv2.getTrackbarPos('Max Saturation', 'Value Control')
    #low_val = cv2.getTrackbarPos('Min Value', 'Value Control')
    #high_val = cv2.getTrackbarPos('Max Value', 'Value Control')

    params = cv2.SimpleBlobDetector_Params()
    params.filterByCircularity = True

    minBlue = 82
    maxBlue = 135
    params.minCircularity = 75.0/100.0
    params.minThreshold = 180
    params.maxThreshold = 200
    params.minArea = 1000
    params.maxArea = 70000
    low_sat = 100
    high_sat = 255
    low_val = 50
    high_val = 255

    # Blob Detector
    detector=cv2.SimpleBlobDetector(params)

    # Get Frame
    blurred_frame = cv2.GaussianBlur(frame, (9, 9), 0)

    # Get Color Mask
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([minBlue, low_sat, low_val])
    upper_blue = np.array([maxBlue, high_sat, high_val])

    color_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    color_mask = cv2.bitwise_not(color_mask)
    keypoints=detector.detect(color_mask)
    cen_point = [320.0, 240.0]
    size = 0.0
    if len(keypoints) > 0:
        k = keypoints[0]
        #l = dir(k)
        #print l
        cen_point = k.pt
        size = k.size

    # We don't really need this image, remove it in final design
    image_wkeys = cv2.drawKeypoints(color_mask, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return cen_point, size, image_wkeys

## How we would call this function
#camera = cv2.VideoCapture(0)
#ret, frame = camera.read()

#p, s, image = blob_detection(frame)
