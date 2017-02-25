import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)


#pins we r gonna use 
ControlPin = [21,20,16,12]

#each pin in controlPin to be output pin and set low
for pin in ControlPin:
    print pin
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)
