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
patch_status = 0
block = 0
lastBlock = 0
def cleanData(raw_data):
	try:
		data = json.loads(raw_data)
		#print 'raw_data: ',data, 'normal'
	except Exception as e:
		#print 'Exception 1:', e
		#print raw_data
		raw_data = raw_data.split('}{')
		raw_data = '{"' + raw_data[-1][1:]
		#print raw_data, "truncated"
		data = json.loads(raw_data)
	return data

def postData(data):
	if data['reading'] == 0:
		return None #don't post it must be ir
	try:
		post(url, data=data)
		#print 'posted', data
	except Exception as e:
		print 'Exception 2', e
		#print "unable to post the data"	

def matUpdate(block):
	global lastBlock
	matUrl = server_address + "matrixUpdate/1/" +str(block)+"/"
	if block == lastBlock:
		return None #don't post
	try:
		get(matUrl)
		lastBlock = block
		print 'bot in', block,
	except Exception as e:
		print e
		
def patchStatus():
	url = server_address + "patchStatus/2/"
	global patch_status
	try: 	
		status = get(url)
		if status.text == "True": patch_status = 1
	except Exception as e:
		print e

def patchStatusUpdate():
	url = server_address + "patchStatusUpdate/1/"
	try:
		get(url)# update the patch status of this robot 
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
				
			matUpdate(block) #get request to update the block position
			patchStatus() #get request to get the patch status of the other bot
						
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
			#print ir_status, ds_status
			time.sleep(.5)
		else:
			print "no raw data from sensors"
			time.sleep(1)


def localisationFuction():
	print "localisation started!!!!"
	url = server_address+"blockCheck/%s/"			
	c1 = get(url %1)
	c2 = get(url %2)
	x1 = int(c1.text[1])
	x2 = int(c2.text[4])
	y1 = int(c1.text[1])
	y2 = int(c1.text[4])
	#got the coordinates of both the bots
	#now check the orientation 
	if y1%2 == 0: moving = "up"
	else: moving = "down"
	print "moving: ", moving
	if moving == "up":
		m = (3/20) * abs(y2-y1)
		n = (3/20) * abs(x1-x2)
		print "x = ",n,"y = ", m 
		if y2<y1:
			print  "y2<y1"
			if x2<x1:
				# move x1-x2 up
				ForwardStep(n)
				print 'localisation: moving forward'
				
			elif x2>x1:
				#move x2-x1 down
				BackwardStep(n)
				print 'localisation: moving backward'

			Left90()
			ForwardStep(m)
			print 'localisation: moving forward'

			#move y1-y2 left
				 
		if y2>y1:
			print "y2>y1"
			if x2<x1:
				#move x1-x2  up 
				ForwardStep(n)
				print 'localisation: moving forward'
	
			elif x2>x1:
				#move x2-x1 down 
				BackwardStep(n)
				print 'localisation: moving backward'

			Right90()
			ForwardStep(m)
			print 'localisation: moving forward'

			#move y2-y1 right
						
	elif moving == "down":
		m = (3/20) * abs(y2-y1)
		n = (3/20) * abs(x1-x2) 
		if y2<y1:
			if x2<x1:
				# move x1-x2 up
				BackwardStep(n)
				
			elif x2>x1:
				#move x2-x1 down
				ForwardStep(n)
				
			Right90()
			ForwardStep(m)
			#move y1-y2 left
				 
		if y2>y1:
			if x2<x1:
				#move x1-x2  down 
				BackwardStep(n)
				
			elif x2>x1:
				#move x2-x1 up 
				ForwardStep(n)
			Left90()
			ForwardStep(m)
			#move y2-y1 right
		

def main():
	flag = True
	forwardCount = 0
	global block, patch_status
	while True:
		try:
			if patch_status: 
				print 'other bot has found the patch, calling localisationFucntion()'
				localisationFuction()
				print 'work done breaking the main function!'
				break
			
			if ir_status:
				print 'Patch found'
				patchStatusUpdate()
				print 'breaking the main function'
				break

			elif ds_status:
				print 'got a wall bro!'
				if flag:
					Left90()
					if patch_status: localisationFuction()
					
					ForwardStep(3) #one full rotation only
					block += 1 #forward += 3
						
					Left90()
					flag = False
					print 'left turn'
				else:
					Right90() 
					if patch_status: localisationFuction()
					
					ForwardStep(3) #one full rotation only
					block += 1 #forward += 3
					Right90()
					flag = True
					print 'right turn '
				
			else:
				print 'Taking ForwardStep()'
				forwardCount +=1 
				if forwardCount == 3:
					block += 1
					forwardCount = 0
				ForwardStep(1)

					
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
