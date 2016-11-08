# import RPi.GPIO as GPIO
import time
# from functions import rc_time, ForwardStep, BackwardStep, Right90, Left90
import json
from socket import socket

listener_address = ('localhost', 6000 )
listener_socket = socket()
listener_socket.connect(listener_address)
print 'listener connected', listener_socket

main_address = ('localhost', 9000 )
main_socket = socket()
main_socket.connect(main_address)
print 'main connected', main_socket

def ldr_process():
    ldr_threshold = 10 # to be caliberated
    while True:
        status = 0
        ldr_reading = int(raw_input('ldr reading :'))
        if ldr_reading > ldr_threshold: # globally defined
            status = 1
        listener_data = json.dumps({'sensor':'ldr','reading': ldr_reading, 'status' : status})
        listener_socket.send(listener_data) #for reading
        try:
            main_socket.send(listener_data) #for msg
        except Exception as e:
            print e
            pass

if __name__ == "__main__":
    try:
        ldr_process()
    except KeyboardInterrupt:
        listener_socket.close()
        main_socket.close()
        print 'closing sockets'
