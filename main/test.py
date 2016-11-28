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
