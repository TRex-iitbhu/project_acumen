import time
from socket import *
# from threading import Thread
import pickle
import thread

listener_address = ('localhost', 6000 )
#Creating socket object
sock = socket()
#binding socket to a address.
sock.bind(listener_address)
#Listening at the address
sock.listen(3) #3 clients can queue

def clientThread(conn):
    while True:
        data = conn.recv(1024) #1kb of data to be received
        if data != '':
            print data

while True:
    #accepting incoming connections
    conn, addr = sock.accept()
    print 'connected :', conn, addr
    thread.start_new_thread(clientThread,(conn,))
#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

conn.close()
sock.close()
