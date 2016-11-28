# import RPi.GPIO as GPIO
from multiprocessing.connection import Client, Pipe
import time
from multiprocessing import Process
# from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
from threading import Thread

address = ('localhost', 6000)
try:
    listener_conn = Client(address, authkey = 'ldr')
except Exception as e:
    print e

# GPIO.setmode(GPIO.BOARD)

def ldr_process(conn):
    ldr_threshold = 10
    while True:
        msg = False
        ldr_reading = int(raw_input('ldr reading:'))
        listener_conn.send(['ldr', ldr_reading]) # send reading to listner.py
        if ldr_reading > ldr_threshold:
            msg = True
            listener_conn.send('patch found')
        conn.send(msg) # to be received in main function

def ds_process(conn):
    ds_threshold = 10
    while True:
        msg = False
        ds_reading = int(raw_input('ds reading: '))
        listener_conn.send(['ds', ds_reading])
        if ds_reading < ds_threshold:
            msg = True
            listener_conn.send('wall ahead')
        conn.send(msg)

def main():

	try:
		if ldr_parent_conn.recv():
			print 'Patch found'
			return None #breaks out of the function

		elif ds_parent_conn.recv():
			#got a wall bro!
			print 'Right90()'
			print 'ForwardStep()' #one full rotation only
			print 'Right90()'
			#Turned around

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

    ds_parent_conn, ds_child_conn = Pipe()
    ldr_parent_conn, ldr_child_conn = Pipe()

    D = Process(target = ds_process(ds_child_conn))
    D.start()
    print 'D started'

    L = Process(target = ldr_process(ldr_child_conn))
    L.start()

    M = Process(target=main())
    M.start()

    L.join()
    M.join()
    D.join()
