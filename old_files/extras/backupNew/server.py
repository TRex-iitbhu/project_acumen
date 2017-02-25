import time
from socket import *
# from threading import Thread
import json
import thread
from requests import post

listener_address = ('localhost', 6000 )
listener_socket = socket()#Creating socket object
listener_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
listener_socket.bind(listener_address) #binding socket to a address.
listener_socket.listen(4) #3 clients can queue #Listening at the address

server_address = "http://192.168.0.5:80/"
url = server_address + "sensor_readings/"

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

def postData(data):
	try:
		post(url, data=data)
		print 'posted', data
	except Exception as e:
		print 'Exception 2', e
		print "unable to post the data"	
	

try:
	sensor_conn, addr = listener_socket.accept()
	print 'server.py connected to', sensor_conn
	while True:
			try:
				raw_data = sensor_conn.recv(4096) #4kb of data to be received
				if raw_data != '':
					data = cleanData(raw_data)
					postData(data)
					
				else: 
					print "no data to listener socket"
					time.sleep(1)
					
					
			except KeyboardInterrupt:
				print 'Exception 3'
				sensor_conn.close()
				listener_socket.close()
				print 'closing sockets'
	
except Exception as e:
	print 'Exception 4', e
	sensor_conn.close()
	listener_socket.close()
	print 'closed sockets'
	



	

