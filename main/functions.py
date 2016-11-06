import RPi.GPIO as GPIO
import time

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
