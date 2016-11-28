# import RPi.GPIO as GPIO
from multiprocessing.connection import Client, Pipe
import time
from multiprocessing import Process
# from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
from threading import Thread


listener_address = ('localhost', 6000)
listener_conn = Client(listener_address, authkey = 'listener')
main_address = ('localhost', 5000)
main_conn = Client(main_address, authkey = 'main')



def ldr_process():
    ldr_threshold = 10 # to be caliberated
    while True:
        msg = False
        ldr_reading = int(raw_input('ldr reading :'))
        listener_conn.send(['ldr', ldr_reading]) # send reading to listner.py
        if ldr_reading > ldr_threshold: # globally defined
            msg = True
        main_conn.send(msg) # to be received in main function

if __name__ == "__main__":


    ldr_process()
