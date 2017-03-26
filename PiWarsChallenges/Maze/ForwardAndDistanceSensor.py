# Simple two DC motor robot class usage example..
# Author: Tony DiCola (adapted by Stefania Saladino)
# License: MIT License https://opensource.org/licenses/MIT
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
import pygame, os, sys, datetime
import RPi.GPIO as GPIO
import datetime
import signal
import smbus
import math
from pygame.locals import *
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
import GianoPi
sys.path.insert(1, os.path.join(sys.path[0], '../../../BerryIMU/python-BerryIMU-gryo-accel-compass'))
from LSM9DS0 import *

bus = smbus.SMBus(1)

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly



#######################################################################################################

mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

def writeGRY(register,value):
        bus.write_byte_data(GYR_ADDRESS, register, value)
        return -1

def readGYRz():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536

#initialise the gyroscope
writeGRY(CTRL_REG1_G, 0b00001111) #Normal power mode, all axes enabled
writeGRY(CTRL_REG4_G, 0b00110000) #Continuos update, 2000 dps full scale
################################# 

atexit.register(turnOffMotors)

gianopirobot = GianoPi.GianoPi()
pygame.init()
pygame.joystick.init()
fpsClock = pygame.time.Clock()
pygame.init()
pygame.joystick.init()
j = pygame.joystick.Joystick(0)
j.init()

fps = 10
maxdistance = 3.
tolerance = 15.
freepathdistance = 140
forspeed = 150 #maximum speed 
turnspeed = 100
turntime=0.01
gotime=0.02

gyroZangle = 0.0
LP = 0.1
PastGyroZ = 0
StartAngle = 0
DiffGyroZangle = 0
DiffThreshold = 3
cnt = 0
Slope = 0.4 # from analysis
stopwhileloop = 1

while(stopwhileloop) :
	
	for e in pygame.event.get(): # iterate over event stack
		if e.type == pygame.locals.JOYBUTTONDOWN: # 10
			if(j.get_button(12)==1): # PS logo central button pressed
				gianopirobot.stop()	
				#execfile("../../../Pimoroni/blinkt/examples/rainbow.py")
				#time.sleep(2)
				stopwhileloop = 0

		rightdistance = gianopirobot.get_rightobjectdistance()
		if((rightdistance >= maxdistance)&(rightdistance<=tolerance)):
			gianopirobot.forward(forspeed, forspeed, gotime)
			rightdistance = gianopirobot.get_rightobjectdistance()
			#print str(rightdistance)
		if(rightdistance>tolerance): # too far from wall
			gianopirobot.stop()
			while (gianopirobot.get_rightobjectdistance() > tolerance): 
				print "more than tolerance - before " + str(gianopirobot.get_rightobjectdistance())
				gianopirobot.turnright_m2_m4(turnspeed, turntime)
				gianopirobot.forward(turnspeed, turnspeed, gotime)
				gianopirobot.turnleft_m2_m4(turnspeed,turntime)
				gianopirobot.goright(forspeed, forspeed, gotime)
				print "after " + str(gianopirobot.get_rightobjectdistance())
				rightdistance = gianopirobot.get_rightobjectdistance()
				#gianopirobot.stop()

		if(rightdistance < maxdistance):
			gianopirobot.stop()
			while (gianopirobot.get_rightobjectdistance() < maxdistance): 
				print "less than max - before " + str(gianopirobot.get_rightobjectdistance())
				gianopirobot.turnleft_m2_m4(turnspeed, turntime)
				gianopirobot.forward(turnspeed, turnspeed, gotime)
				gianopirobot.turnright_m2_m4(turnspeed,turntime)
				gianopirobot.goleft(forspeed, forspeed,gotime)
				print "after " + str(gianopirobot.get_rightobjectdistance())
				rightdistance = gianopirobot.get_rightobjectdistance()
				#gianopirobot.stop()

	
		#cnt = cnt + 1


	
