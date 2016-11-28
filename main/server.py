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
		print raw_data
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
	
def clientThread(conn):
	print "Thread started"
	while True:
		try:
			raw_data = conn.recv(1024) #1kb of data to be received
			if raw_data != '':
				data = cleanData(raw_data)
				postData(data)
				
			else: print "no data to listener socket"
				
		except KeyboardInterrupt:
			print 'Exception 3'
			conn.close()
			listener_socket.close()
			print 'closing sockets'

count = 0

try:
	ds_conn, addr = listener_socket.accept()#will wait for a new conn to proceed below
	print 'server.py connected to', ds_conn
	thread.start_new_thread(clientThread,(ds_conn,)) 
except Exception as e:
	print 'Exception 4', e
try:
#accepting incoming connections
	ir_conn, addr = listener_socket.accept()#will wait for a new conn to proceed below
	print 'server.py connected to ', ir_conn
	thread.start_new_thread(clientThread,(ir_conn,)) #will run parallel with main()
except Exception as e:
	print 'Exception 5', e
	
while True:
	pass
#to run the program with the threads
