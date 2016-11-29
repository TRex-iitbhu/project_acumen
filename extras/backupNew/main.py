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

def cleanData(raw_data):
	try:
		data = json.loads(raw_data)
		print 'raw_data: ',data, 'normal'
	except Exception as e:
		print 'Exception 1: json loading exception', e
		#print raw_data
		raw_data = raw_data.split('}{')
		raw_data = '{"' + raw_data[-1][1:]
		print raw_data, "truncated"
		data = json.loads(raw_data)
	return data
	
def SensorThread(conn):
	while True:
		global ir_status, ds_status
		raw_data = conn.recv(1024) #1kb of data to be received
		if raw_data != '':
			data = cleanData(raw_data)
			status = data['status']
			if data['sensor'] == 'ir': ir_status = status
			elif data['sensor'] == 'ds':  ds_status = status
			print ir_status, ds_status
			time.sleep(.5)
		else:
			print "no raw data from sensors"
			time.sleep(1)


def main():
	try:
		if ir_status:
			print 'Patch found'
			return True 

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
		sensor_conn.close()
		print "closed"
		return 'break'

try:
#accepting incoming connections
	sensor_conn, addr = main_socket.accept()#will wait for a new conn to proceed below
	print 'main.py connected :', sensor_conn
	thread.start_new_thread(SensorThread,(sensor_conn,)) #will run parallel with main()
except Exception as e:
	print 'Exception 1', e

	
while True:
	try:
		if main()=='break':
			
			main_socket.close()
			sensor_conn.close()
	
			GPIO.cleanup()
			print "Breaking main function!"
			time.sleep(.100)
			break
			

	except KeyboardInterrupt:
		print 'Exception 3'
		main_socket.close()
		sensor_conn.close()
		GPIO.cleanup()
