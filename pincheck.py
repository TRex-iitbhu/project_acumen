import RPi.GPIO as GPIO
import time
import itertools


ControlPinList = [26,19,13,6]
ControlPins = itertools.permutations(ControlPinList)
for j,ControlPin in enumerate(list(ControlPins)):
    
    print 'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'
    print ControlPin
    GPIO.setmode(GPIO.BCM)    
    for pin in ControlPin:
        print pin
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,0)
        
    seq = [ [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1],

        ]

    for i in range(512):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(ControlPin[pin], seq[halfstep][pin])

            time.sleep(0.001)
                    
    GPIO.cleanup()
    #cleanup to reset all the pins once the program ends!
    print str(j) + '  DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
