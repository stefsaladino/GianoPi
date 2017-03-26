import os, sys
import time
import atexit
import RPi.GPIO as GPIO
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
import GianoPi

M1_TRIM = 0
M2_TRIM = 0
M3_TRIM = 0
M4_TRIM = -70 #today 15/01/2017

GPIO.setmode(GPIO.BCM)

# the following are  the pins connected from the Pi on the ADC
SPICLK = 19 
SPIMISO = 20 
SPIMOSI = 12 
SPICS = 25 

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

gianopirobot = GianoPi.GianoPi(m1_trim=-10, m2_trim=M2_TRIM, m3_trim=M3_TRIM, m4_trim=M4_TRIM)

MiddleSensors = [1,1]

#gianopirobot.forward(50)
TURNSPEED = 60
SIDESPEED = 80
SPEED = 100
BLACK = 900

while(True):
    
    gianopirobot.forward(SPEED)
    MiddleSensors = gianopirobot.read_ch1_ch2_from_adc(MiddleSensors)

    while (MiddleSensors[0] <= BLACK)&(MiddleSensors[1] > BLACK):
        gianopirobot.turnleft_m2_m4(TURNSPEED, seconds=0.1)
        MiddleSensors = gianopirobot.read_ch1_ch2_from_adc(MiddleSensors)

    while (MiddleSensors[0] > BLACK)&(MiddleSensors[1] <= BLACK):
        gianopirobot.turnright_m2_m4(TURNSPEED, seconds=0.1)
        MiddleSensors = gianopirobot.read_ch1_ch2_from_adc(MiddleSensors)
    
    while (MiddleSensors[0] <= BLACK)&(MiddleSensors[1] <= BLACK):
        gianopirobot.stop()
        #print "STOP, ", line_sensors[1],line_sensors[2]

        
atexit.register(gianopirobot.stop())
GPIO.cleanup()

