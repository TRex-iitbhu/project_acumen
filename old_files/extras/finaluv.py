import time
import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print "distance measurement"

 
temperature = 20
speedSound = 33100 + (0.6 * temperature)

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG,False)




def measure():
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    start = time.time()
    while GPIO.input(ECHO)==0:
        start = time.time()

    while GPIO.input(ECHO)==1:
        stop = time.time()

    elapsed = stop - start

    distance = (elapsed*speedSound)/2
    distance = round(distance,2)
    return distance
    
try:

    while True:
        distance = measure()
        print distance
        time.sleep(1)

except KeyboardInterrupt:

    GPIO.cleanup()

    




        
