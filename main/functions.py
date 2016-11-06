import RPi.GPIO as GPIO
import time

'''
LDR
'''
def rc_time(pin):
    count=0

    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)
    time.sleep(0.001)

    #back to input
    GPIO.setup(pin, GPIO.IN)

    #count until the pin goes high
    while (GPIO.input(pin) == GPIO.LOW):
        count += 1

    return count

'''
Distance Sensor
'''
#to be written

'''
STEPPER
'''

#randomly choosen
RControlPin = [26, 19, 6, 13)] #right motor pins
LControlPin = [6, 9, 14, 12] #left motor pins
FLed = 2
GPIO.setup(FLed, GPIO.OUT)
GPIO.output(FLed, 0)


#All pins set to output and to zero
for r,l in zip(RControlPin, LControlPin):
    GPIO.setup(r, GPIO.OUT)
    GPIO.setup(l, GPIO.OUT)
    GPIO.output(r, 0)
    GPIO.output(l, 0)

seq = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1],
    ]


circumference = 2 * 3.1417 * r

def Right90():
    '''
    WL --> forward by n rotations
    WR --> backward by n rotations
    simultaneously with same speed.

    '''
# n to be calculated acc to circumference etc

    for i in range(n * 512): # 1 rotation
        for halfstep in range(8): #we have 8 halfsteps
            for pin in range(4): #we have 4 pins to loop through
                GPIO.output(RControlPin[pin], seq[halfstep][pin])
                GPIO.output(LControlPin[pin], seq[-halfstep][pin])#to be tested.
            time.sleep(0.001)
    '''
    extra steps logic to be written
    '''

def Left90():
    pass

'''
ForwardStep = 1 rotation forward
BackwardStep = 1 rotation backward
'''

def ForwardStep():

    GPIO.output(FLed, 1)

    for i in range(512): # 1 rotation
        for halfstep in range(8): #we have 8 halfsteps
            for pin in range(4): #we have 4 pins to loop through
                GPIO.output(RControlPin[pin], seq[halfstep][pin])
                GPIO.output(LControlPin[pin], seq[halfstep][pin])
            time.sleep(0.001)
            '''
            LDR logic
            '''

    GPIO.output(FLed, 0)

def BackwardStep(distance):
    for i in range(512): # 1 rotation
        for halfstep in range(8): #we have 8 halfsteps
            for pin in range(4): #we have 4 pins to loop through
                GPIO.output(RControlPin[pin], seq[-halfstep][pin])
                GPIO.output(LControlPin[pin], seq[-halfstep][pin])
            time.sleep(0.001)

'''
Suppose there's an object in front of bot, what could it either be
wall or other bot
bot1: dimension L*L cms
if wall: for bot1(see arena pic ) turn to its left by 90 --> then move forward by L/2.
'''
