import RPi.GPIO as GPIO
import time
from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90, distanceMeasure
from socket import socket
import json

listener_address = ('localhost', 6000 )
listener_socket = socket()
listener_socket.connect(listener_address)
print "server connected: " ,listener_socket, ' connected'

main_address = ('localhost', 7000 )
main_socket = socket()
main_socket.connect(main_address)
print "main connected ", main_socket, ' connected'

GPIO.setmode(GPIO.BCM)

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
				print listener_data
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
