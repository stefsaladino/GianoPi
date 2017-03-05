# Simple two DC motor robot class usage example..
# Author: Tony DiCola (adapted by Stefania Saladino)
# License: MIT License https://opensource.org/licenses/MIT
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
import pygame, os, sys, datetime
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
import RPi.GPIO as GPIO
import datetime
import signal
import GianoPi

#######################################################################################################


mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    GPIO.cleanup()


atexit.register(turnOffMotors)

################################# 

forspeed = 150 #maximum speed 
backspeed = 100

MotorTwo = mh.getMotor(2)
MotorFour = mh.getMotor(4)

MotorTwo.run(Adafruit_MotorHAT.FORWARD) #M1
MotorFour.run(Adafruit_MotorHAT.BACKWARD) #M4

gianopirobot = GianoPi.GianoPi()

maxdistance = 5.

while(True) :

	if(gianopirobot.get_leftobjectdistance() > maxdistance):
		gianopirobot.forward(forspeed)
	else:
		gianopirobot.backward(backspeed, 0.01)
		gianopirobot.stop()

	
	

	
