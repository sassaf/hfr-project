import cv2
import color_editing

color = 'blue'
colors_list = [color]

camera = cv2.VideoCapture(0);

ret = True;

while (ret):
    ret, frame = camera.read()

    ######

    blurred_frame = cv2.GaussianBlur(frame, (9, 9), 0)
    img_gray = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

    color_frames = color_editing.setting_colors(blurred_frame, colors_list)
    c_count = "0"

    name = color
    color_mask = color_frames[name]
    c_count = cv2.countNonZero(color_mask)
    c_count_string = str(cv2.countNonZero(color_mask))
    filtered_frame = cv2.bitwise_and(frame, frame, mask=color_mask) # now only [name] color portions of screen will show, in its color

    ######

    frame = filtered_frame
    imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if type(contours) is not None:
        if len(contours)>0:
            print len(contours)
            cnt = contours[0]
            cv2.drawContours(frame, [cnt], 0, (0,255,0), 3)

    #cv2.imshow("Image", image)
    cv2.imshow("Image With Contours", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q'):
        ret = False
        cv2.destroyAllWindows()

camera.release()