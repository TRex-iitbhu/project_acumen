import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

TRIG = 23                                  #Associate GPIO pin 16 to TRIG
ECHO = 24                                   #Associate GPIO pin 18 to ECHO


print "Distance measurement in progress"

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in


while True:

  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  print "Waitng For Sensor To Settle"
  time.sleep(1)                            #Delay of 2 seconds

  print 'settled'
  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(1)                            #Delay of 0.00001 seconds
                                           #Set TRIG as LOW
  GPIO.output(TRIG, False)
                  
  print 'TRIG sent'
  print 'checking echo'
  

  while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
    pulse_start = time.time()              #Saves the last known time of LOW pulse

  print 'echo not zero'
  
  i = 0
  while i<400:
      print GPIO.input(ECHO)
      i += 1
      
      
  while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
    pulse_end = time.time()                #Saves the last known time of HIGH pulse 

  print 'echo not one'
  
  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            #Round to two decimal points

  if distance > 2 and distance < 400:      #Check whether the distance is within range
    print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
  else:
    print "Out Of Range"                   #display out of range
  
  
