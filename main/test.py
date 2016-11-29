from functions import irMeasure, ForwardStep, BackwardStep, Right90, Left90, distanceMeasure
from requests import get
server_address = 'http://192.168.0.5/'
#Right90()
#ForwardStep(3)
#print distanceMeasure()
#print irMeasure()
def localisationFuction():
	url = server_address+"blockCheck/%s/"			
	c1 = get(url %1)
	c2 = get(url %2)
	x1 = int(c1.text[1])
	x2 = int(c2.text[4])
	y1 = int(c1.text[1])
	y2 = int(c1.text[4])
	print x1,x2,y1,y2

localisationFuction()
