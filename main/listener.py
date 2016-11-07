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
		msg = conn.recv()
        if msg[0] == 'ldr':
			print 'ldr reading: ' , msg[1]
			#post request to the server
		elif msg[0] == 'ds':
			print 'ds reading: ', msg[1]
			#post request to the server
		elif msg=='patch found':
			print msg
			#post request to the server
except KeyboardInterrupt:
    pass
