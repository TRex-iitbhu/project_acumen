import subprocess

subprocess.Popen('listener.py', shell=True)
print '1'
subprocess.Popen('main.py', shell=True)
print '2'

subprocess.Popen('ds.py', shell=True)
print'3'
