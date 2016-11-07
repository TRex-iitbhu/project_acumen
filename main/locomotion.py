import RPi.GPIO as GPIO
from multiprocessing.connection import Client
import time

from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90

address = ('localhost', 6000)
conn = Client(address, authkey='ldr')

GPIO.setmode(GPIO.BOARD)

ControlPin = 40

try:
    while True:
        ldr_reading = rc_time(ControlPin)
        print 'Reading LDR'
        conn.send(ldr_reading)
        if ldr_reading > ldr_threshold:
            print 'Patch found'
            break
        else:
            ds_reading = Distance() #to be done
            if ds

except KeyboardInterrupt:
    pass
finally:
    print 'cleaning up'
    GPIO.cleanup()
