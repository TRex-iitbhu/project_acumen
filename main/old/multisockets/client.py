from socket import *

address = ('localhost', 6000 )

sock = socket()
sock.connect(address)
while True:
    data = sock.send(raw_input('data : '))

sock.close()
