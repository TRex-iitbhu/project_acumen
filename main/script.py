import subprocess

subprocess.Popen('python listener.py', shell=True)
print '1'
subprocess.Popen('python main.py', shell=True)
print '2'
subprocess.Popen('python ds.py', shell=True)
print'3'
