# import RPi.GPIO as GPIO
import time
# from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
import time
from socket import socket
import thread
import json

main_address = ('localhost', 9000 )
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
			# break


# GPIO.setmode(GPIO.BOARD)
def main():

	if ldr_status:
		print 'Patch found'
		return True #breaks out of the function

	elif ds_status:
		#got a wall bro!
		# Right90()
		# ForwardStep() #one full rotation only
		# Right90()
		print 'Turned around'
		return False
	else:
		print 'ForwardStep()'
		return False


	# finally:
	# 	print 'cleaning up'
	# 	# GPIO.cleanup()

#accepting incoming connections
ldr_conn, addr = main_socket.accept()#will wait for a new conn to proceed below
print 'LDR CONNECTED'
print 'connected :', ldr_conn, addr
thread.start_new_thread(clientThread,(ldr_conn,)) #will run parallel with main()

ds_conn, addr = main_socket.accept()#will wait for a new conn to proceed below
print 'DS CONNECTED'
print 'connected :', ldr_conn, addr
thread.start_new_thread(clientThread,(ds_conn,)) #will run parallel with main()

while True:
	if main():
		print 'PATCH FOUND!!!'
		break
	time.sleep(1)

conn.close()
main_socket.close()
