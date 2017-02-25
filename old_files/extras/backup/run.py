from sys import executable
import time
from subprocess import call, Popen
'''
Popen([executable, 'server.py'], shell=True)
#print "running listener"

Popen([executable, 'main.py'], shell=True)
#print "running main"

Popen([executable, 'ldr.py'],shell=True)
#print "running ldr"

Popen([executable, 'ds.py'], shell=True)
print "running ds"

import os
os.system("python server.py")
print 'listener'
os.system("python main.py")
print 'main'



ps -fA | grep python




execfile('server.py')
execfile('main.py')
execfile('ds.py')



'''

try:
	call(['lxterminal', '-e', 'python server.py'])
	print 'server.py running'
except Exception as e:
	print e
time.sleep(1)
try:
	call(['lxterminal', '-e', 'python main.py'])
	print "main.py running"
	
except Exception as e:
	print e
time.sleep(1)

try:
	call(['lxterminal', '-e', 'python ir.py'])
	print "ir.py running"
except Exception as e:
	print e
time.sleep(1)
try:
	call(['lxterminal', '-e', 'python ds.py'])
	print "ds.py running"
except Exception as e:
	print e
	
while True:
	try:
		pass
	except KeyboardInterrupt:
		break
