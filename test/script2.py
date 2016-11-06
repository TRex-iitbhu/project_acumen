
from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey='secret password')
while True:
    inp = raw_input()
    conn.send(inp)
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()
