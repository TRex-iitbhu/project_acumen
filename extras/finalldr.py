import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

PIN_OUT = 4


def ReadingLDR(PIN_OUT):
    reading = 0

    GPIO.setup(PIN_OUT,GPIO.OUT)
    GPIO.output(PIN_OUT,GPIO.LOW)

    time.sleep(0.001)

    GPIO.setup(PIN_OUT,GPIO.IN)

    while GPIO.input(PIN_OUT)==GPIO.LOW:
        reading += 1

    return reading

# main program

try:
    while True:
        print ReadingLDR(PIN_OUT)
        time.sleep(0.00001)
        

except KeyboardInterrupt:
    GPIO.cleanup()


    
