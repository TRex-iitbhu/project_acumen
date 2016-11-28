import time
from socket import *
# from threading import Thread
import json
import thread
from requests import post

listener_address = ('localhost', 6000 )
sock = socket()#Creating socket object
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sock.bind(listener_address) #binding socket to a address.
sock.listen(3) #3 clients can queue #Listening at the address

server_address = "http://192.168.0.5:80/"
url = server_address + "sensor_readings/"

def cleanData(raw_data):
	try:
		data = json.loads(raw_data)
		print 'raw_data: ',data, 'normal'
	except Exception as e:
		print 'json loading exception', e
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
		print e
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
			conn.close()
			sock.close()
			print 'closing sockets'

count = 0
while True:
	try:#accepting incoming connections
		conn, addr = sock.accept()
		print 'server.py connected with :', conn
		print 'thread starting for this socket'
		thread.start_new_thread(clientThread,(conn,))#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		
	except KeyboardInterrupt:
		print "closing sockets"
		conn.close()
		sock.close()
		print "closed"
