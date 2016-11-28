import RPi.GPIO as GPIO
import time
from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
import time
from socket import socket
import thread
import json
GPIO.setmode(GPIO.BCM)

main_address = ('localhost', 7000 )
main_socket = socket()
main_socket.bind(main_address)
main_socket.listen(3) #3 clients can queue

ldr_status = 0
ds_status = 0

def clientThread(conn):
	while True:
		global ldr_status, ds_status
		raw_data = conn.recv(1024) #1kb of data to be received
		if raw_data != '':
			data= json.loads(raw_data)

			if data['sensor'] == 'ldr':
			    ldr_status = data['status']

			elif data['sensor'] == 'ds':
			    ds_status = data['status']

			print ldr_status, ds_status
			time.sleep(.1)
			# break
		else:
			print "no raw data from sensors"


def main():
	try:

		if ldr_status:
			print 'Patch found'
			return True #breaks out of the function

		elif ds_status:
			print 'got a wall bro!'
			Right90()
			ForwardStep() #one full rotation only
			Right90()
			print 'Turned around'
			return False
		else:
			print 'Taking ForwardStep()'
			ForwardStep()
			return False
			
	except KeyboardInterrupt:
		print "closing sockets"
		main_socket.close()
		ldr_conn.close()
		ds_conn.close()
		print "closed"
		return 'break'

	# finally:
	# 	print 'cleaning up'
	# 	# GPIO.cleanup()
try:
#accepting incoming connections
	ldr_conn, addr = main_socket.accept()#will wait for a new conn to proceed below
	print 'main.py connected :', ldr_conn
	thread.start_new_thread(clientThread,(ldr_conn,)) #will run parallel with main()
except Exception as e:
	print e
try:
	ds_conn, addr = main_socket.accept()#will wait for a new conn to proceed below
	print 'main.py connected :', ds_conn
	thread.start_new_thread(clientThread,(ds_conn,)) #will run parallel with main()
except Exception as e:
	print e
	
while True:
	try:
		if main()=='break':
			break

		time.sleep(.1)

	except KeyboardInterrupt:
		main_socket.close()
		GPIO.cleanup()
