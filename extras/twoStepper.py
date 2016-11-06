import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)    
ControlPin1 = [26,19,13,6]
ControlPin2 = [21,20,16,12]

for pin in ControlPin1+ControlPin2:
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


for i in range(10*512):
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(ControlPin1[pin], seq[-halfstep][pin])
            GPIO.output(ControlPin2[pin], seq[-halfstep][pin])
#            time.sleep(0.100)
        time.sleep(0.001)
                
GPIO.cleanup()


