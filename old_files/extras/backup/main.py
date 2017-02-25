import RPi.GPIO as GPIO
import time
from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
import time
from socket import *
import thread
import json
GPIO.setmode(GPIO.BCM)

main_address = ('localhost', 7000 )
main_socket = socket()
main_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
main_socket.bind(main_address)
main_socket.listen(3) #3 clients can queue

ir_status = 0
ds_status = 0

def clientThread(conn):
	while True:
		global ir_status, ds_status
		raw_data = conn.recv(1024) #1kb of data to be received
		if raw_data != '':
			data= json.loads(raw_data)

			if data['sensor'] == 'ir':
			    ir_status = data['status']

			elif data['sensor'] == 'ds':
			    ds_status = data['status']

			print ir_status, ds_status
			time.sleep(.500)
			# break
		else:
			print "no raw data from sensors"


def main():
	try:
		if ir_status:
			print 'Patch found'
			return 'break' #breaks out of the function

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
		ir_conn.close()
		ds_conn.close()
		print "closed"
		return 'break'

try:
#accepting incoming connections
	ir_conn, addr = main_socket.accept()#will wait for a new conn to proceed below
	print 'main.py connected :', ir_conn
	thread.start_new_thread(clientThread,(ir_conn,)) #will run parallel with main()
except Exception as e:
	print 'Exception 1', e
try:
	ds_conn, addr = main_socket.accept()#will wait for a new conn to proceed below
	print 'main.py connected :', ds_conn
	thread.start_new_thread(clientThread,(ds_conn,)) #will run parallel with main()
except Exception as e:
	print 'Exception 2', e
	
while True:
	try:
		if main()=='break':
			
			main_socket.close()
			ir_conn.close()
			ds_conn.close()
			GPIO.cleanup()
			print "Breaking main function!"
			time.sleep(10)
			break
			

	except KeyboardInterrupt:
		print 'Exception 3'
		main_socket.close()
		ir_conn.close()
		ds_conn.close()
		GPIO.cleanup()
