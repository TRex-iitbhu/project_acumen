# import RPi.GPIO as GPIO
import time
# from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
import time
from socket import *
import thread
import pickle

main_address = ('localhost', 9000 )
main_socket = socket()
main_socket.bind(main_address)
main_socket.listen(3) #3 clients can queue

ldr_status = False
ds_status = False

def clientThread(conn):
	while True:
		global ldr_status, ds_status
		data = conn.recv(1024) #1kb of data to be received
		if data != '':
			print data
		# if data[0] == 'ldr':
		#     ldr_status = data[1]
		# elif data[0] == 'ds':
		#     ds_status = data[1]

while True:
	#accepting incoming connections
	conn, addr = main_socket.accept()
	print 'connected :', conn, addr
	thread.start_new_thread(clientThread,(conn,))

conn.close()
sock.close()

# GPIO.setmode(GPIO.BOARD)
def main():

	try:
		if ldr_status:
			print 'Patch found'
			return None #breaks out of the function

		elif ds_status:
			#got a wall bro!
			# Right90()
			# ForwardStep() #one full rotation only
			# Right90()
			print 'Turned around'
			main() #repeat

		else:
			print 'ForwardStep()'
			main() #RECURSION IT IS!!!!#FFFFFF


	except KeyboardInterrupt:
		pass

	finally:
		print 'cleaning up'
		# GPIO.cleanup()

if __name__ == '__main__':

	main()
