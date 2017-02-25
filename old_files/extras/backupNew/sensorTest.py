from __future__ import print_function
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
'''
RControlPin = [6,13,19,26] #right motor pins
LControlPin = [21,20,16,12] #left motor pins


#All pins set to output and to zero
for r,l in zip(RControlPin, LControlPin):
    GPIO.setup(r, GPIO.OUT)
    GPIO.setup(l, GPIO.OUT)
    GPIO.output(r, 0)
    GPIO.output(l, 0)
   
'''
RControlPin = [6,13,19,26] #right motor pins
LControlPin = [21,20,16,12] #left motor pins

RControlPin.reverse()
LControlPin.reverse()

#All pins set to output and to zero
for r,l in zip(RControlPin, LControlPin):
    GPIO.setup(r, GPIO.OUT)
    GPIO.setup(l, GPIO.OUT)
    GPIO.output(r, 0)
    GPIO.output(l, 0)



TRIG = 7
ECHO = 8

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG,False)


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

for i in range(10):
	print (distanceMeasure(TRIG, ECHO))
	time.sleep(.4)


seq = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1],
    ]


while True:
	for i in range(512): # 1 rotation
		for halfstep in range(8): #we have 8 halfsteps
			for pin in range(4): #we have 4 pins to loop through
				GPIO.output(RControlPin[pin], seq[halfstep][pin])
				GPIO.output(LControlPin[pin], seq[halfstep][pin])
			time.sleep(0.001)

GPIO.cleanup()


