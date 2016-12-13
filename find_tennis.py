import cv2
import numpy
import color_editing
import serial
import RXTX
import blob_detection

camera = cv2.VideoCapture(0);

color = 'blue'
colors_list = [color]

ret, frame = camera.read()
count=0

while (ret):
    ret, frame = camera.read()
    blurred_frame = cv2.GaussianBlur(frame, (9, 9), 0)
    img_gray = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)

    color_frames = color_editing.setting_colors(blurred_frame, colors_list)
    c_count = "0"

    name = color
    color_mask = color_frames[name]
    c_count = cv2.countNonZero(color_mask)
    c_count_string = str(cv2.countNonZero(color_mask))
    filtered_frame = cv2.bitwise_and(frame, frame, mask=color_mask) # now only [name] color portions of screen will show, in its color

    name = name[0].upper() + name[1:len(name)]

    nothing=False

    #Initialize values
    left = 1
    right = 1
    speed=(0,0) #left, right

    if (c_count < 500):
        speed = (0,0)
        nothing=True
        #nothing
    elif (c_count >15000):
        #reverse
        speed = (200,200)
        left = 0
        right = 0
    elif (c_count < 10000):
        speed = (200,200)
        left = 1
        right = 1
        #drive
    else:
        speed=(0,0)
        #nothing



    ##PID


    #error = Pixels want - Pixels_Actual

    #if count < 20
        #ErrArray[count]=error
    #elif
        #ErrArray

    #count++

    #Kp=1
    #Ki=0
    #Kd=0


    #P= Kp*error
    #I=Ki*numpy.trapz(ErrArray)

    #for n in ErrArray
        #slope[n]=numpy.diff(ErrArry,n)

    #D=Kd*sum(slope)/len(slope)

    #output = P=I+D
    #speed= 255*output


    #turning
    left_turn_roi=color_mask[ 0:480, 0:200]
    left_count = cv2.countNonZero(left_turn_roi)

    no_turn_roi=color_mask[ 0:480, 200:400]
    no_count = cv2.countNonZero(no_turn_roi)

    right_turn_roi=color_mask[ 0:480, 440:640]
    right_count = cv2.countNonZero(right_turn_roi)


    if ((not nothing) and (left_count > right_count) and (left_count > no_count)):
        #turn left yo
        speed = (150,150)
        left = 1
        right = 0

    if ((not nothing) and (right_count > left_count) and (right_count > no_count)):
        #turn right yo
        right = 1
        left = 0
        speed = (150,150)

    cv2.putText(filtered_frame, str(speed), (0,400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, 8)
    cv2.putText(filtered_frame, c_count_string, (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, 8)
    cv2.imshow("{} Filtered Frame".format(name), filtered_frame)
    cv2.imshow('Full Color Image', frame)

    ser = RXTX.send_arduino(left, right, speed[0], speed[1])

    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q'):
        ret = False
        cv2.destroyAllWindows()

camera.release()
ser.close()

