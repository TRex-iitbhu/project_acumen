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

server_address = "http://192.168.1.103:80/"
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
		url = server_address + "sensor_readings/2/"
		post(url, data=data)
		#print 'posted', data
	except Exception as e:
		print 'Exception 2', e
		#print "unable to post the data"	

def matUpdate(block):
	global lastBlock
	matUrl = server_address + "matrixUpdate/2/" +str(block)+"/" #/1/ for bot 1
	if block == lastBlock: #not first block, initially block=lastblock but i want to show that too.
		return None #don't post
	try:
		get(matUrl)
		lastBlock = block
		print 'bot in', block
	except Exception as e:
		print e
		
def patchStatus(): #check patch status of bot 1
	url = server_address + "patchStatus/1/" #/2/ for bot 1
	global patch_status
	try: 	
		status = get(url)
		if status.text == "True": patch_status = 1
	except Exception as e:
		print e

def patchStatusUpdate(): #update own patch status
	url = server_address + "patchStatusUpdate/2/1/" #/1/ for bot 1
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
	global block
	print "localisation started!!!!"
	url = server_address+"blockCheck/%s/"			
	c1 = get(url %1)
	c2 = get(url %2)
	x1 = int(c1.text[1])
	x2 = int(c2.text[1])
	y1 = int(c1.text[4])
	y2 = int(c2.text[4])
	print x1, y1, "and ", x2, y2
	#got the coordinates of both the bots
	#now check the orientation 
	if y2%2 == 0: moving = "down"
	else: moving = "up"
	print "moving: ", moving
	m = 3 * abs(y2-y1)
	n = 3 * abs(x1-x2)
	if moving == "up":
		print "x = ",abs(x1-x2),"y = ", abs(x1-x2) 
		if y2<y1:
			print  "y2<y1"
			if x2<x1:
				# move x1-x2 up
				print 'localisation: moving forward'
				ForwardStep(n)
				block += n
				
			elif x2>x1:
				#move x2-x1 down
				print 'localisation: moving backward'
				BackwardStep(n)
				block -= n
				
			print 'turning left90'
			Left90()
			print 'localisation: moving forward'
			ForwardStep(m)
			

			#move y1-y2 left
				 
		if y2>y1:
			print "y2>y1"
			if x2<x1:
				#move x1-x2  up 
				print 'localisation: moving forward'
				ForwardStep(n)
				block += n
				
	
			elif x2>x1:
				#move x2-x1 down 
				print 'localisation: moving backward'
				BackwardStep(n)
				block -= n
				
			print 'turning Right90'
			Right90()
			print 'localisation: moving forward'
			ForwardStep(m)
			

			#move y2-y1 right
						
	elif moving == "down":
		if y2<y1:
			if x2<x1:
				# move x1-x2 up
				print 'taking backward step'
				BackwardStep(n)
				
			elif x2>x1:
				#move x2-x1 down
				print 'taking forward step'
				ForwardStep(n)
			
			print 'taking right 90'
			Right90()
			print 'taking forward step '
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
				patchStatusUpdate()
				print 'updating patch status'
				print 'work done breaking the main function!'
				break
			
			elif ir_status:
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
					print 'taking Forward step'
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
	url = server_address + "patchStatusUpdate/2/0/" #/1/ for bot 1
	try:
		get(url)# update the patch status of this robot as 0
		print 'patch status set to False'
		url = server_address + "sensor_readings/2/"
		post(url, data={'sensor':'ir', 'reading':'0','status':'0'})
		print 'IR status set to False'
		matUrl = server_address + "matrixUpdate/2/0/"
		print 'initial block set as 0'
	except Exception as e:
		print e
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
