import RPi.GPIO as GPIO
from multiprocessing.connection import Client
import time
from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90

address = ('localhost', 6000)
listener_conn = Client(address, authkey = 'ldr')
ldr_threshold = 100000 # to be caliberated
ds_threshold = 10 # to be caliberated
GPIO.setmode(GPIO.BOARD)

def ldr_process(conn):
    while True:
        msg = False
        ldr_reading = rc_time()
        listener_conn.send(['ldr', ldr_reading]) # send reading to listner.py
        if ldr_reading > ldr_threshold # globally defined
            msg = True
        conn.send(msg) # to be received in main function

def ds_process(conn):
    while True:
        msg = False
        ds_reading = Distance()
        listener_conn.send(['ds', ds_reading])
        if ds_reading < ds_threshold:
            msg = True
        conn.send(msg)

def main():

	try:
		if ldr_parent_conn.recv():
			print 'Patch found'
			return None #breaks out of the function

		elif ds_parent_conn.recv():
			#got a wall bro!
			Right90()
			ForwardStep() #one full rotation only
			Right90()
			#Turned around

			main() #repeat

		else:
			ForwardStep()
			main() #RECURSION IT IS!!!!#FFFFFF


	except KeyboardInterrupt:
		pass

	finally:
		print 'cleaning up'
		GPIO.cleanup()

if __name__ == '__main__':

    ldr_parent_conn, ldr_child_conn = Pipe()
    L = Process(target = ldr_process(ldr_child_conn))
    L.start()

    ds_parent_conn, ds_child_conn = Pipe()
    D = Process(target = ds_process(ds_child_conn))
    D.start()

    M = Process(target=main())
    M.start()

    L.join()
    M.join()
    D.join()
