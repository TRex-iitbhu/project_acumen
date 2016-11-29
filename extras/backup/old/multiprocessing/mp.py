from multiprocessing import Process, Queue, Pipe
import time

'''
Queue
'''
def f(q):
	for i in range(10):
		q.put(i)
		print 'put', i

if __name__ == '__main__':
	q = Queue()
	p = Process(target=f, args=(q,))
	p.start()
	for i in range(10):
		time.sleep(.3)
		print q.get()

	p.join()

'''
Pipe()
'''
# def f(conn):
# 	for i in range(100):
# 		conn.send(i)
# 		print 'sent', i
# 	conn.close()
#
# if __name__ == '__main__':
#
# 	parent_conn, child_conn = Pipe()
# 	p = Process(target=f, args=(child_conn,))
# 	p.start()
# 	for i in range(100):
# 		time.sleep(.3)
# 		print parent_conn.recv()
#
# 	p.join()


















# def f(q):
#     q.put([42, None, 'hello'])
# def f2(q):
# 	for i in range(1000):
# 		q.append([i])
#
# if __name__ == '__main__':
# 	q = Queue()
# 	p = Process(target=f, args=(q,)) #call function f with q as arg
# 	p.start()
# 	print(q.get())    # prints "[42, None, 'hello']"
# 	r = Process(target=f2, args=(q,))
# 	r.start()
# 	print(q.get())
# 	r.join()
# 	p.join()
