# import RPi.GPIO as GPIO
import time
# from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
from socket import socket
import json

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

        status = 0
        ds_reading = int(raw_input('ds reading: '))
        if ds_reading < ds_threshold:
            status = 1
        listener_data = json.dumps({'sensor':'ds','reading': ds_reading, 'status' : status})
        listener_socket.send(listener_data) #for reading
        main_socket.send(listener_data) #for msg

if __name__ == "__main__":
    try:
        ds_process()
    except KeyboardInterrupt:
        listener_socket.close()
        main_socket.close()
        print 'sockets closed'
