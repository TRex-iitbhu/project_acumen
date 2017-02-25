import RPi.GPIO as GPIO
from socket import socket
import json
import time
GPIO.setmode(GPIO.BCM)


listener_address = ('localhost', 6000 )
listener_socket = socket()
listener_socket.connect(listener_address)
print "server connected: " ,listener_socket, ' connected'

main_address = ('localhost', 7000 )
main_socket = socket()
main_socket.connect(main_address)
print "main connected ", main_socket, ' connected'


pins = [14,18,17]
GPIO.setup(15,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.output(15,1)
GPIO.output(27,1)

for i in pins:
    GPIO.setup(i, GPIO.IN)
while True:
	time.sleep(1)
	try:
		a = []
		for i in pins:
			a.append(GPIO.input(i))
		status = 1 if 1 in a else 0
		try:
			listener_data = json.dumps({'sensor':'ir','reading': a, 'status' : status})
			listener_socket.send(listener_data) #for reading
			main_socket.send(listener_data)
			print 'sent', a
		except Exception as e:
			print 'Exception 1',e
		
	except Exception as e:
		print 'Exception 2',e
		main_socket.close()
		listener_socket.close()
		GPIO.cleanup() 
		print 'closing sockets'       



    









        

