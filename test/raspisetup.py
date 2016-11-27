from sys import executable
from subprocess import call, Popen
'''
Popen([executable, 'listener.py'], shell=True)
#print "running listener"

Popen([executable, 'main.py'], shell=True)
#print "running main"

Popen([executable, 'ldr.py'],shell=True)
#print "running ldr"

Popen([executable, 'ds.py'], shell=True)
print "running ds"

import os
os.system("python listener.py")
print 'listener'
os.system("python main.py")
print 'main'
'''

'''
ps -fA | grep python


'''


'''
execfile('listener.py')
execfile('main.py')
execfile('ds.py')


execfile('sensorTest.py')

execfile('printtest.py')
'''

call(['lxterminal', '-e', 'python server.py'])
call(['lxterminal', '-e', 'python main.py'])
call(['lxterminal', '-e', 'python ldr.py'])
call(['lxterminal', '-e', 'python ds.py'])
