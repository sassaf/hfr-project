import cv2
import numpy as np


camera = cv2.VideoCapture(0);

ret = True
while (ret):
    ret,img = camera.read()

    blurred_img = cv2.GaussianBlur(img, (9, 9), 0)
    img_gray = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, img_gray.shape[1]/8,
                               param1=130, param2=50, minRadius=5)

    print circles
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(img_gray,(i[0],i[1]),i[2],(255,255,255),2)
            # draw the center of the circle
            cv2.circle(img_gray,(i[0],i[1]),2,(255,255,255),3)

    cv2.imshow('detected circles', img_gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        ret = False
        cv2.destroyAllWindows()

cv2.destroyAllWindows()