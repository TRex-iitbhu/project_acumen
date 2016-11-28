import time
from multiprocessing.connection import Listener
address = ('localhost', 6000)
listener = Listener(address, authkey='listener')

main_conn = listener.accept()
print 'connection accepted from' , listener.last_accepted
ldr_conn = listener.accept()
print 'connection accepted from' , listener.last_accepted
ds_conn = listener.accept()
print 'connection accepted from' , listener.last_accepted

try:
    while True:
        ldr_msg = ldr_conn.recv()
        print ldr_msg
        main_msg = main_conn.recv()
        print main_msg
        ds_msg = ds_conn.recv()
        print ds_msg
        print main_msg, ldr_msg, ds_msg
        # if msg[0] == 'ldr':
        #     print 'ldr reading: ' , msg[1]
        #     #post request to the server
        # elif msg[0] == 'ds':
        #     print 'ds reading: ', msg[1]
        #     #post request to the server
        # elif msg=='patch found':
        #     print msg
        #     #post request to the server
        # elif msg == 'wall ahead':
        #     print msg
except KeyboardInterrupt:
    pass
