import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
import time
from socket import socket
import json



pins = [14,18,17]
GPIO.setup(15,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.output(15,1)
GPIO.output(27,1)

for i in pins:
    GPIO.setup(i, GPIO.IN)

while True:
	try:
		a = []
		for i in pins:
			a.append(GPIO.input(i))
		print a
		time.sleep(1)

	except Exception as e:
		GPIO.cleanup()        



    









        

