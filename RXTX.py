# This code uses pyserial to connect to the serial port
# It sends a sequence of inputs to the serial port
# Then it reads in data and prints it to the screen
#
# Useful commands:
# inputString = ser.readline()
# ser.write("output string")
## Conversion
# floatInput = float(inputString)
# intInput = int(inputString)
# numericInput = float(x) if '.' in x else int(x) #For unknown inputs
##
# ord('a') # = 65
# chr(65)   # = 'A'

#portName = 'COM6' # Windows will look like this
portName = '/dev/ttyACM0' #Unix looks like this
baudRate = 115200


import serial
from time import sleep
delay = .1 # the arduino seems to be sensitive to this number around .2

ser = serial.Serial(portName,baudRate)

sleep(3) # give the micro controller a little time to set up

print "Begin python tx/rx script"

# Using rxString protocol
ser.write("{0,0,0")

# Read the data then print it to the terminal
def send_arduino(leftDirection, rightDirection, leftSpeed, rightSpeed):
    #inString = ser.readline()
    #print inString

    # Prompt for input
    # Example input: 1 1 255 255  straight full power
    # Example input: 1 0 255 0    turn right
    #leftDirection = input("left direction: enter 1 or 0")
    #rightDirection = input("right direction: enter 1 or 0")
    #leftSpeed = input("left speed: enter 0 to 255")
    #rightSpeed = input("right speed: enter 0 to 255")

    # Perform filtering
    # direction can be 0 or 1, speed is 0 to 255
    leftSpeed = int(leftSpeed)
    rightSpeed = int(rightSpeed)
    if (leftDirection > 1 or leftDirection < 0):
            leftDirection = 0
    if (rightDirection > 1 or rightDirection < 0):
            rightDirection = 0
    if (leftSpeed > 255 or leftSpeed < 0):
            leftSpeed = 0
    if (rightSpeed > 255 or rightSpeed < 0):
            rightSpeed = 0


    # direction is 0b00 00 00 LR where L and R are the direction bits
    direction = leftDirection << 1 | rightDirection
    	
    # Format the string
    output = "{" + str(direction) + "," + str(leftSpeed) + "," + str(rightSpeed)

    # Print to terminal then arduino
    print output
    ser.write(output)
    return ser

# Closing the stream is a good idea but the while loop never reaches here	
#ser.close()















