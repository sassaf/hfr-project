import cv2
import numpy as np
#import serial
import RXTX
import blob_detection
import time

camera = cv2.VideoCapture(0);

ret, frame = camera.read()
motor_speed=0

#if robot loses sight of target, this variable calcs time since last seen
#time_since=0
#timeinitial=time.clock()
#a=timeinitial
#b=0
last_size = 0
no_object = False
timer = 0
spin_timer = 0
full_turn=False
followed_last_location = False
last_positive = False

integral=[]

speed = (0,0)
left = 1
right = 1
while(ret):
    st = time.clock()
    ret, frame = camera.read()
    #Garbage Frames, call and discard
    for x in range(1,4):
        camera.grab()
    position, size, blobframe = blob_detection.find(frame)
    #definitions

    stop_size = 50.0
    center = 320
    kp=4
    ki=0.08
    kpturn=0.7
    cv2.imshow('blobs', blobframe)

    if (size > 0):
        followed_last_location = False

    Error = size - stop_size

    #calculate Integral
    if len(integral) < 20:
        integral.append(Error)
    else:
        temp = [Error]
        integral = temp + integral[0:19]

    I=ki*np.trapz(integral)
    #PID Output Forward/Backwards
    P=kp*Error

    output=P+I


    print output

    #Set Speed Limits
    motor_speed=np.absolute(output)
    if (Error == -stop_size):
        no_object = True
    elif (motor_speed > 175):
        no_object = False
        last_size = size

        motor_speed = 175
        speed = (motor_speed, motor_speed)
    elif(motor_speed <90):
        no_object = False
        last_size = size

        motor_speed = 90
        speed = (motor_speed, motor_speed)



    direction = np.sign(output)

    if (direction == -1 and not (Error == -stop_size)):
        last_positive = True
        left = 1
        right = 1

        #PID Turning, Forward only currently
        if not position[0] == 320.0:
            turnE= position[0]-center

            turnvariable=turnE*kpturn

            #if positive turn right, negative turn left

            speed = [motor_speed+turnvariable, motor_speed-turnvariable]
            #bounds for left motor
            if (speed[0]> 200):
                speed[0] = 200
            elif(speed[0] <90):
                speed[0] = 90
             #bounds for right motor
            if (speed[1]> 200):
                speed[1] = 200
            elif(speed[1] <90):
                speed[1] = 90


    elif (direction == +1):
        last_positive = False
        left = 0
        right = 0




    if (not followed_last_location):
        if (no_object and (timer == 0)):
            start_time = time.clock()
            if last_size != 0:
                #arbitrarily choose 0 speed as new speed
                #speed =(speed[0], speed[0])
                one_sec_size = 90
                timer = one_sec_size/last_size
                timer = timer*(speed[0]/175.0)
        elif (no_object and (timer > 0)):
            time_diff = time.clock() - start_time
            if (time_diff > timer):
                timer = 0
                speed = (0,0)
                followed_last_location = True

    if (last_positive):
        left = 1
        right = 1
    else:
        left = 0
        right = 0

    #if (no_object and (direction == -1)):
        #if (followed_last_location and (not full_turn) and (spin_timer<=0)):
            #print "spin to win"
            #spin_start_time = time.clock()
            #left = 1
            #right = 0
            #speed = (125,125)
            #spin_timer = 5.5
        #elif (spin_timer > 0):
            #spin_diff = time.clock() - spin_start_time
            #print spin_diff
            #print spin_timer
            #left = 1
            #right = 0
            #speed = (125,125)
            #if (spin_diff > spin_timer):
                #spin_timer = 0
                #full_turn = True
                #speed = (0,0)
    #else:
        #full_turn = False

    st - time.clock()

    if ((direction == -1) and (np.abs(Error)<7)):
        speed = (0,0)
    elif ((direction == +1) and (np.abs(Error)<10)):
        speed = (0,0)

    ser = RXTX.send_arduino(left, right, speed[0], speed[1])

    #Turning

    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.waitKey(1) & 0xFF == ord('Q'):
        ret = False
        cv2.destroyAllWindows()
        ser = RXTX.send_arduino(left, right, 0, 0)

camera.release()