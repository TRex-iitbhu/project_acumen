from __future__ import print_function
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

'''
LDR
'''
ldrPin = 40

def rc_time(ldrPin):
    count=0

    GPIO.setup(ldrPin,GPIO.OUT)
    GPIO.output(ldrPin,0)
    time.sleep(0.001)

    #back to input
    GPIO.setup(ldrPin, GPIO.IN)

    #count until the pin goes high
    while (GPIO.input(ldrPin) == GPIO.LOW):
        count += 1

    return count

'''
Distance Sensor
'''

def distanceMeasure(TRIG, ECHO):

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    start = time.time()
    while GPIO.input(ECHO)==0:
        start = time.time()

    while GPIO.input(ECHO)==1:
        stop = time.time()

	elapsed = stop - start
	temperature = 20
	speedSound = 33100 + (0.6 * temperature)
    distance = (elapsed*speedSound)/2
    distance = round(distance,2)
    return distance
   

'''
STEPPER
'''

#randomly choosen
#RControlPin = [26, 19, 6, 13] #right motor pins
#LControlPin = [6, 9, 14, 12] #left motor pins
RControlPin = [6,13,19,26] #right motor pins
LControlPin = [21,20,16,12] #left motor pins
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

#n is number of rotations of stepper needed for 90 degree rotation of bot

def Right90():
    '''
    WL --> forward by n rotations
    WR --> backward by n rotations
    simultaneously with same speed.

    '''
# n to be calculated acc to circumference etc

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

    for i in range(n * 512): # 1 rotation
        for halfstep in range(8): #we have 8 halfsteps
            for pin in range(4): #we have 4 pins to loop through
                GPIO.output(RControlPin[pin], seq[-halfstep][pin])
                GPIO.output(LControlPin[pin], seq[halfstep][pin])#to be tested.
            time.sleep(0.001)

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

    GPIO.output(FLed, 0)

def BackwardStep(distance):
    for i in range(512): # 1 rotation
        for halfstep in range(8): #we have 8 halfsteps
            for pin in range(4): #we have 4 pins to loop through
                GPIO.output(RControlPin[pin], seq[-halfstep][pin])
                GPIO.output(LControlPin[pin], seq[-halfstep][pin])
            time.sleep(0.001)
'''
while True:
	try:
		for i in range(512): # 1 rotation
			for halfstep in range(8): #we have 8 halfsteps
				for pin in range(4): #we have 4 pins to loop through
					GPIO.output(RControlPin[pin], seq[halfstep][pin])
					GPIO.output(LControlPin[pin], seq[halfstep][pin])

				time.sleep(0.001)
	except KeyboardInterrupt:
		GPIO.cleanup()
'''
