import RPi.GPIO as GPIO
from socket import *
import thread

import json
import time
from functions import irMeasure, ForwardStep, BackwardStep, Right90, Left90, distanceMeasure

GPIO.setmode(GPIO.BCM)

def ds():
	ds_threshold = 10	 # to be caliberated
	while True:
		try:
			status = 0
			ds_reading = distanceMeasure()
			if ds_reading < ds_threshold:status = 1 
			
			data = json.dumps({'sensor':'ds','reading': ds_reading, 'status' : status}) # data as str
			try:
				listener_socket.send(data) #for reading
				main_socket.send(data) #for msg
				print 'sent through ds() ', data
				time.sleep(1)
			except Exception as e:
				print 'Exception 1', e
				time.sleep(1)	
			
		except Exception as e:
			print 'Exception 2', e
			print "closing the sockets"
			listener_socket.close()
			main_socket.close()
			print "closed the sockets"
				


def ir():
	while True:
		try:
			reading = irMeasure()
			status = 1 if reading>0 else 0
			try:
				data = json.dumps({'sensor':'ir','reading': reading, 'status' : status})
				listener_socket.send(data) #for reading
				main_socket.send(data)
				print 'sent through ir() ', data
				time.sleep(1)
			except Exception as e:
				print 'Exception 4',e
				time.sleep(1)
			
		except Exception as e:
			print 'Exception 5',e
			main_socket.close()
			listener_socket.close()
			print 'closed sockets'       



listener_address = ('localhost', 6000 )
listener_socket = socket()
listener_socket.connect(listener_address)
print "sensor connected to listener: " ,listener_socket, ' connected'

main_address = ('localhost', 7000 )
main_socket = socket()
main_socket.connect(main_address)
print "sensor connected to main", main_socket, ' connected'


try:
	thread.start_new_thread(ir,())
except Exception as e:
	print 'Exception 6', e

time.sleep(.5)

try:
	ds()
except Exception as e:
	print 'Exception 7', e
	









        

