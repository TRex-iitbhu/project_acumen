import RPi.GPIO as GPIO
import time
from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90, distanceMeasure
from socket import socket
import json

listener_address = ('localhost', 6000 )
listener_socket = socket()
listener_socket.connect(listener_address)
print listener_socket, 'connected'

main_address = ('localhost', 9876 )
main_socket = socket()
main_socket.connect(main_address)
print main_socket, 'connected'
GPIO.setmode(GPIO.BCM)


TRIG = 7
ECHO = 8

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG,False)

   
def ds_process():
    ds_threshold = 10 # to be caliberated
    while True:
		try:
			status = 0
			ds_reading = distanceMeasure(TRIG, ECHO)
			if ds_reading < ds_threshold:
				status = 1
			listener_data = json.dumps({'sensor':'ds','reading': ds_reading, 'status' : status})
			listener_socket.send(listener_data) #for reading
			main_socket.send(listener_data) #for msg
			time.sleep(.3)
		except:
			listener_socket.close()
			main_socket.close()
			
if __name__ == "__main__":
    try:
        ds_process()
    except KeyboardInterrupt:
        listener_socket.close()
        main_socket.close()
        print 'sockets closed'
