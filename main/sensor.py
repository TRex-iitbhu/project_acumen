import RPi.GPIO as GPIO
from socket import *
import thread

import json
import time
from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90, distanceMeasure

GPIO.setmode(GPIO.BCM)

def ds():
	TRIG = 7
	ECHO = 8

	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	GPIO.output(TRIG,False)

	   
	def ds_process():
		ds_threshold = 10 # to be caliberated
		print "threshold set"
		while True:
			try:
				status = 0
				ds_reading = distanceMeasure(TRIG, ECHO)
				if ds_reading < ds_threshold:
					status = 1
				listener_data = json.dumps({'sensor':'ds','reading': ds_reading, 'status' : status}) # data as str
				try:
					listener_socket.send(listener_data) #for reading
					main_socket.send(listener_data) #for msg
					print 'sent through ds() ', listener_data
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
				

	try:
		ds_process()
	except KeyboardInterrupt:
		print 'Exception 3'
		listener_socket.close()
		main_socket.close()
		print 'sockets closed'


def ir():
	pins = [14,18,17]
	GPIO.setup(15,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)
	GPIO.output(15,1)
	GPIO.output(27,1)

	for i in pins:
		GPIO.setup(i, GPIO.IN)
	while True:
		try:
			a = 0
			for i in pins:
				a+= GPIO.input(i)
			status = 1 if a>0 else 0
			try:
				listener_data = json.dumps({'sensor':'ir','reading': a, 'status' : status})
				listener_socket.send(listener_data) #for reading
				main_socket.send(listener_data)
				print 'sent through ir() ', listener_data
				time.sleep(1)
			except Exception as e:
				print 'Exception 4',e
				time.sleep(1)
			
		except Exception as e:
			print 'Exception 5',e
			main_socket.close()
			listener_socket.close()
			GPIO.cleanup() 
			print 'closing sockets'       



listener_address = ('localhost', 6000 )
listener_socket = socket()
listener_socket.connect(listener_address)
print "server connected: " ,listener_socket, ' connected'

main_address = ('localhost', 7000 )
main_socket = socket()
main_socket.connect(main_address)
print "main connected ", main_socket, ' connected'


try:
	thread.start_new_thread(ir,())
except Exception as e:
	print 'Exception 6', e

time.sleep(.5)

try:
	ds()
except Exception as e:
	print 'Exception 7', e
	









        

