from multiprocessing import Process
from threading import Thread
import time

def forLoop():
	print time.time()
	for i in range(1000):
		print i
	print time.time()
	
def forloop2():
	print time.time()
	for i in range(146):
		print 'halwa'
	print time.time()
	
if __name__ == '__main__':
	Thread(target=forLoop()).start()
	Thread(target=forloop2()).start()


''''
q = Process(target=forloop2())
p = Process(target=forLoop(10))
q.start()
p.start()
p.join()

'''
