import time
from socket import *
# from threading import Thread
import json
import thread

listener_address = ('localhost', 6000 )
#Creating socket object
sock = socket()
#binding socket to a address.
sock.bind(listener_address)
#Listening at the address
sock.listen(3) #3 clients can queue

def clientThread(conn):
    ldr_reading, ds_reading = 0, 0
    while True:
        raw_data = conn.recv(1024) #1kb of data to be received
        if raw_data != '':
            data = json.loads(raw_data)
            if data['sensor'] == 'ldr':
                ldr_reading = data['reading']

            elif data['sensor'] == 'ds':
                ds_reading = data['reading']

            print 'ldr_reading: ', ldr_reading,' , ds_reading: ', ds_reading


while True:
    #accepting incoming connections
    conn, addr = sock.accept()
    print 'connected :', conn, addr
    thread.start_new_thread(clientThread,(conn,))
#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

conn.close()
sock.close()
