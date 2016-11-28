# import RPi.GPIO as GPIO
from multiprocessing.connection import Client,Listener
import time
# from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90

listener_address = ('localhost', 6000)
listener_conn = Client(listener_address, authkey = 'listener')

main_address = ('localhost', 5000)
listener = Listener(main_address, authkey='main')
ldr_conn = listener.accept()
print 'connection accepted from' , listener.last_accepted
ds_conn = listener.accept()
print 'connection accepted from' , listener.last_accepted

# GPIO.setmode(GPIO.BOARD)



def main():

	try:
		if ldr_conn.recv():
			print 'Patch found'
			return None #breaks out of the function

		elif ds_conn.recv():
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
