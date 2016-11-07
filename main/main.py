import RPi.GPIO as GPIO
from multiprocessing.connection import Client
import time

from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90

address = ('localhost', 6000)
conn = Client(address, authkey='ldr')

GPIO.setmode(GPIO.BOARD)

ldrPin = 40
def main():
	
	try:
		
		ldr_reading = rc_time(ldrPin)
		conn.send(['ldr', ldr_reading])
		
		if ldr_reading > ldr_threshold:
			print 'Patch found'
			conn.send(['patch_found'])
			break
			
		else:
			ds_reading = Distance() #to be done
			conn.send(['ds', ds_reading])
			
			if ds_reading < ds_threshold:
				#got a wall bro!
				Left90()
				ForwardStep()
				Left90()
				
				main() #repeat
				
			else:
				ForwardStep()
				main() #RECURSION IT IS!!!!#FFFFFF
					 

	except KeyboardInterrupt:
		pass
		
	finally:
		
		print 'cleaning up'
		GPIO.cleanup()
