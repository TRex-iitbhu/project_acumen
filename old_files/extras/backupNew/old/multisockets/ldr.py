# import RPi.GPIO as GPIO
import time
# from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
from socket import *

listener_address = ('localhost', 6000 )
listener_socket = socket()
listener_socket.connect(listener_address)
print listener_socket, 'connected'

main_address = ('localhost', 9000 )
main_socket = socket()
main_socket.connect(main_address)
print main_socket, 'connected'

def ldr_process():
    ldr_threshold = 10 # to be caliberated
    while True:
        msg = False
        ldr_reading = int(raw_input('ldr reading :'))
        listner_socket.send('ldr_reading:' + str(ldr_reading)) # send reading to listner.py
        if ldr_reading > ldr_threshold: # globally defined
            msg = True
        main_socket.send('ldr status:' + str(msg)) # to be received in main function

if __name__ == "__main__":
    ldr_process()
    sock.close()
