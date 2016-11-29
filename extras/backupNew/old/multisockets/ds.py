# import RPi.GPIO as GPIO
import time
# from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
from socket import *
import pickle

listener_address = ('localhost', 6000 )
listener_socket = socket()
listener_socket.connect(listener_address)
print listener_socket, 'connected'

main_address = ('localhost', 9000 )
main_socket = socket()
main_socket.connect(main_address)
print main_socket, 'connected'

def ds_process():
    ds_threshold = 10 # to be caliberated
    while True:
        msg = False
        ds_reading = int(raw_input('ds reading: '))
        listener_socket.send('ds_reading:' + str(ds_reading))
        if ds_reading < ds_threshold:
            msg = True
        main_socket.send('ds status:' + str(msg))

if __name__ == "__main__":
    try:
        ds_process()
    except KeyboardInterrupt:
        pass
