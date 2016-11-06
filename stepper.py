import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


#pins we r gonna use 
ControlPin = [7,11,13,15]

#each pin in controlPin to be output pin and set low
for pin in ControlPin:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

#two dimension array 'seq' holds eight step sequence of halfstepping
seq = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1],

    ]


'''
this for loop is used to cycle through sequence a given no. of times
In this case 512 cycles (times of for loop) == 1 revolution
inside motor :
    8 cycles = 1 revolution
outside motor:
    becaues of gear reduction = 1/64, 8*64 = 512 cycles = 1 revolution
'''
for i in range(512):
    for halfstep in range(8): #we have 8 halfsteps
        for pin in range(4): #we have 4 pins to loop through
            GPIO.output(ControlPin[pin], seq[halfstep][pin])

        time.sleep(0.001)
#time delay outside the for loop, it means that the pins are first all set, then there's is pause in the program.
#without this delay the coils will be turned ON/OFF at a rate too fast to the magnetic core to response.--> no rotation then.

GPIO.cleanup()
#cleanup to reset all the pins once the program ends!
