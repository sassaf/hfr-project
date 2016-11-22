import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('Value Control')

cv2.createTrackbar('Min Blue', 'Value Control', 82, 180, nothing)
cv2.createTrackbar('Max Blue', 'Value Control', 135, 180, nothing)
cv2.createTrackbar('Min Circularity', 'Value Control', 75, 100, nothing)
cv2.createTrackbar('Min Threshold', 'Value Control',180, 255, nothing)
cv2.createTrackbar('Max Threshold', 'Value Control',200, 255, nothing)
cv2.createTrackbar('Min Saturation', 'Value Control',100, 255, nothing)
cv2.createTrackbar('Max Saturation', 'Value Control',255, 255, nothing)
cv2.createTrackbar('Min Value', 'Value Control',50, 255, nothing)
cv2.createTrackbar('Max Value', 'Value Control',255, 255, nothing)

camera = cv2.VideoCapture(0);

ret, frame = camera.read()

params=cv2.SimpleBlobDetector_Params()
params.filterByCircularity=True

detector=cv2.SimpleBlobDetector(params)


while (ret):

    # Trackbar Values
    minBlue = cv2.getTrackbarPos('Min Blue', 'Value Control')
    maxBlue = cv2.getTrackbarPos('Max Blue', 'Value Control')
    params.minCircularity = cv2.getTrackbarPos('Min Circularity', 'Value Control')/100.0
    params.minThreshold = cv2.getTrackbarPos('Min Threshold', 'Value Control')
    params.maxThreshold = cv2.getTrackbarPos('Max Threshold', 'Value Control')
    low_sat = cv2.getTrackbarPos('Min Saturation', 'Value Control')
    high_sat = cv2.getTrackbarPos('Max Saturation', 'Value Control')
    low_val = cv2.getTrackbarPos('Min Value', 'Value Control')
    high_val = cv2.getTrackbarPos('Max Value', 'Value Control')

    # Blob Detector

    detector=cv2.SimpleBlobDetector(params)

    # Get Frame
    #ret, frame = camera.read()
    frame = cv2.imread("BlobTest.jpg", cv2.IMREAD_GRAYSCALE)
    blurred_frame = cv2.GaussianBlur(frame, (9, 9), 0)

    # Get Color Mask
    #hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    #lower_blue = np.array([minBlue, low_sat, low_val])
    #upper_blue = np.array([maxBlue, high_sat, high_val])

    #color_mask = cv2.inRange(hsv, lower_blue, upper_blue)


    #filtered_frame = cv2.bitwise_and(frame, frame, mask=color_mask)
    #color_mask = cv2.bitwise_not(color_mask)
    color_mask=frame
    keypoints=detector.detect(color_mask)

    image_key = cv2.drawKeypoints(color_mask, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    #cv2.imshow('Color Frame', filtered_frame)
    cv2.imshow('Original', frame)
    cv2.imshow('Blobs', image_key)

    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q'):
        ret = False
        cv2.destroyAllWindows()

camera.release()