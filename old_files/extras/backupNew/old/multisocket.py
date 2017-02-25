import time
from socket import *
from threading import *
import thread
address1 = ('localhost', 6000 )
sock1 = socket()
sock1.bind(address1)
sock1.listen(3) #3 clients can queue

address2 = ('localhost', 9000 )
sock2 = socket()
sock2.bind(address2)
sock2.listen(3) #3 clients can queue

def clientThread(conn):
    while True:
        data = conn.recv(1024) #1kb of data to be received
        print data

while True:
    #accepting incoming connections
    conn1, addr = sock1.accept()
    print 'connected ', conn1, addr
    thread.start_new_thread(clientThread,(conn1,))#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.

    conn2, addr = sock2.accept()
    print 'connected ', conn2, addr
    thread.start_new_thread(clientThread,(conn2,))

conn1.close()
sock1.close()

conn2.close()
sock2.close()
