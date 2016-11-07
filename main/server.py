from functions import rc_time
import RPi.GPIO as GPIO
import time


from multiprocessing.connection import Listener
address = ('localhost', 6000)
listener = Listener(address, authkey='ldr')
conn = listener.accept()
print 'connection accepted from' , listener.last_accepted

try:
    while True:
        print conn.recv()
except KeyboardInterrupt:
    pass
