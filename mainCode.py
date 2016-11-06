import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#randomly choosen
RControlPin = [7, 11, 13, 15] #right motor pins
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
    for i in n: #n rotations
        for i in range(512): # 1 rotation
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
'''
for halfstep in range(8):
    for pin in range(4): #we have 4 pins to loop through
        GPIO.output(RControlPin[pin], seq[halfstep][pin])
        GPIO.output(LControlPin[pin], seq[halfstep][pin])

#IS EQUIVALENT TO -
# try to understand the sense:

for halfstep in range(8):
    GPIO.output(RControlPin[0],seq[halfstep][0])
    GPIO.output(RControlPin[1],seq[halfstep][1])
    GPIO.output(RControlPin[2],seq[halfstep][2])
    GPIO.output(RControlPin[3],seq[halfstep][3])

    GPIO.output(LControlPin[0],seq[halfstep][0])
    GPIO.output(LControlPin[1],seq[halfstep][1])
    GPIO.output(LControlPin[2],seq[halfstep][2])
    GPIO.output(LControlPin[3],seq[halfstep][3])

'''




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

#MAIN FUNCTIONS
while True:
    ForwardStep()
    '''
    check if patch is found
    check other bot's status.
    '''

    '''
    US logic
    '''
