import GianoPi
import time
import atexit
import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BCM)

# the following are  the pins connected from the Pi on the ADC
Grove1 = 19 
Grove2 = 20 


# set up the SPI interface pins
GPIO.setup(Grove1, GPIO.IN)
GPIO.setup(Grove2, GPIO.IN)

gianopirobot = GianoPi.GianoPi()

while(True):
    if GPIO.input(Grove1):
        print "Grove 1 is HIGH" 
    else:
        print " Grove 1 is LOW"
    if GPIO.input(Grove2):
        print "Grove 2 is HIGH" 
    else:
        print " Grove 2 is LOW"


#gianopirobot.forward(50)
TURNSPEED =100
SPEED = 200
BLACK = 1
WHITE = 0
   

GPIO.cleanup()

