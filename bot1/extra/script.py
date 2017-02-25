import subprocess

subprocess.Popen('python listener.py', shell=True)
print '1'
subprocess.Popen('python main.py', shell=True)
print '2'
subprocess.Popen('python ds.py', shell=True)
print'3'


from sys import executable
from subprocess import call, Popen, CREATE_NEW_CONSOLE
Popen([executable, 'listener.py'], creationflags=CREATE_NEW_CONSOLE)
print "running listener"
Popen([executable, 'main.py'], creationflags=CREATE_NEW_CONSOLE)
print "running main"
Popen([executable, 'ldr.py'], creationflags=CREATE_NEW_CONSOLE)
print "running ldr"
Popen([executable, 'ds.py'], creationflags=CREATE_NEW_CONSOLE)
print "running ds"

# global f
# f = True
# def function():
#     global f
#     f = False
#     print f
# print f
#
# function()
#
# print f
