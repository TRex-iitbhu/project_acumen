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


def ds_process():
    ds_threshold = 10 # to be caliberated
    while True:
        msg = False
        ds_reading = int(raw_input('ds reading: '))
        listener_conn.send(['ds', ds_reading])
        if ds_reading < ds_threshold:
            msg = True
        main_conn.send(msg)

if __name__ == "__main__":

    ds_process()
