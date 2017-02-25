from functions import irMeasure, ForwardStep, BackwardStep, Right90, Left90, distanceMeasure
from requests import get
import RPi.GPIO as GPIO

server_address = 'http://192.168.0.5/'
import time
#Right90()


	#print distanceMeasure()
#	time.sleep(1)
while True:
	print irMeasure()
	time.sleep(1)
ForwardStep(3)
