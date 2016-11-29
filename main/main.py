import RPi.GPIO as GPIO
import time
from functions import  ForwardStep, BackwardStep, Right90, Left90
from requests import post,get
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

listener_address = ('localhost', 6000 )
listener_socket = socket()#Creating socket object
listener_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
listener_socket.bind(listener_address) #binding socket to a address.
listener_socket.listen(3) #3 clients can queue #Listening at the address

server_address = "http://192.168.0.5:80/"
url = server_address + "sensor_readings/"
ir_status = 0
ds_status = 0
row = 0
col = 0

def cleanData(raw_data):
	try:
		data = json.loads(raw_data)
		#print 'raw_data: ',data, 'normal'
	except Exception as e:
		#print 'Exception 1:', e
		#print raw_data
		raw_data = raw_data.split('}{')
		raw_data = '{"' + raw_data[-1][1:]
		print raw_data, "truncated"
		data = json.loads(raw_data)
	return data

def postData(data):
	try:
		post(url, data=data)
		print 'posted', data
	except Exception as e:
		print 'Exception 2', e
		#print "unable to post the data"	

def matUpdate(row,col):
	matUrl = server_address + "matrixUpdate/1/" +str(row)+"/"+str(col)+"/"
	try:
		get(matUrl)
	except Exception as e:
		print e
	
def listener(sensor_conn):#post the data to the server
	while True:
		try:
			raw_data = sensor_conn.recv(4096) #4kb of data to be received
			if raw_data != '':
				data = cleanData(raw_data)
				postData(data)
				
			else: 
				print "no data to listener socket"
				time.sleep(1)
				
			matUpdate(row,col)
						
		except KeyboardInterrupt:
			print 'Exception 3'
			sensor_conn.close()
			listener_socket.close()
			print 'closing sockets'                                                                                                              
		

def SensorThread(sensor_conn):#update the sensor statuses
	while True:
		global ir_status, ds_status
		raw_data = sensor_conn.recv(1024) #1kb of data to be received
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
	flag = True
	forwardCount = 0
	while True:
		try:
			if ir_status:
				print 'Patch found'
				print 'breaking the main function'
				break

			elif ds_status:
				print 'got a wall bro!'
				if flag:
					Left90()
					ForwardStep(3) #one full rotation only
					Left90()
					flag = False
					print 'left turn'
				else:
					Right90()
					ForwardStep(3)
					Right90()
					flag = True
					print 'right turn '
			else:
				print 'Taking ForwardStep()'
				ForwardStep(1)
				forwardCount +=1 
				if forwardCount == 3:
					row = row % 3 + 1
		except KeyboardInterrupt:
			print "closing sockets"
			main_socket.close()
			sensor_conn.close()
			print "closed"
			break

try:
	sensor_conn, addr = listener_socket.accept()
	print 'listener connected to sensor ', sensor_conn
	thread.start_new_thread(listener,(sensor_conn,))
except Exception as e:
	print 'Exception 0', e

try:
#accepting incoming connections
	sensor_conn, addr = main_socket.accept()#will wait for a new conn to proceed below
	print 'main connected to sensor :', sensor_conn
	thread.start_new_thread(SensorThread,(sensor_conn,)) #will run parallel with main()
except Exception as e:
	print 'Exception 1', e
	

try:
	main()
	'''
	if main()=='break':
		
		main_socket.close()
		sensor_conn.close()

		GPIO.cleanup()
		print "Breaking main function!"
		time.sleep(.100)
		break
	'''
except KeyboardInterrupt:
	print 'Exception 3'
	main_socket.close()
	sensor_conn.close()
	listener_socket.close()
	GPIO.cleanup()
