import RPi.GPIO as GPIO
import time
from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey='ldr')

GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)

ControlPin = 40
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


try:
    while True:
        reading = rc_time(ControlPin)
        print reading
        conn.send(reading)
except KeyboardInterrupt:
    pass
finally:
    print 'cleaning up'
    GPIO.cleanup()

