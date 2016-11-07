from multiprocessing import Process
from threading import Thread
import time

def forLoop(n):
	for i in range(n):
		print i
	print time.time()
def forloop2():
	for i in range(10):
		print 'halwa'
	print time.time()
if __name__ == '__main__':
	Thread(target=forLoop(10)).start()
	Thread(target=forloop2()).start()


''''
q = Process(target=forloop2())
p = Process(target=forLoop(10))
q.start()
p.start()
p.join()

'''
