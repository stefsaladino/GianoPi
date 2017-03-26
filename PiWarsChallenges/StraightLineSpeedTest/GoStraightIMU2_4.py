# Simple two DC motor robot class usage example..
# Author: Tony DiCola (adapted by Stefania Saladino)
# License: MIT License https://opensource.org/licenses/MIT
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
import RPi.GPIO as GPIO
import signal
import smbus
import math
import os, sys

sys.path.insert(1, os.path.join(sys.path[0], '../../../BerryIMU/python-BerryIMU-gryo-accel-compass'))
from LSM9DS0 import *

bus = smbus.SMBus(1)

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly

#######################################################################################################

mh = Adafruit_MotorHAT(addr=0x60)
f = open("GoStraightIMU.txt", 'a')

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    f.close()	

atexit.register(turnOffMotors)

################################# 

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

gyroZangle = 0.0
LP = 0.1
PastGyroZ = 0
StartAngle = 0
DiffGyroZangle = 0
DiffThreshold = 3
cnt = 0
Slope = 0.4 # from analysis
InverseSlope = 1./Slope 

maxspeed = 220 #maximum speed 

MotorTwo = mh.getMotor(2)
MotorFour = mh.getMotor(4)


MotorTwo.run(Adafruit_MotorHAT.BACKWARD) #M2
MotorFour.run(Adafruit_MotorHAT.FORWARD) #M4

speed2 = maxspeed
speed4 = maxspeed


while(True) :

	MotorTwo.setSpeed(int(speed2)) #M2
	MotorFour.setSpeed(int(speed4)) #M4
	time.sleep(LP)
	
	#Read the gyroscope values 
	GYRz = readGYRz()

	#Convert Gyro raw to degrees per second	
	rate_gyr_z =  GYRz * G_GAIN

	#Calculate the angles from the gyro. 
	gyroZangle+=rate_gyr_z*LP

	if(cnt==0):
		StartAngle = gyroZangle
 		print "start angle " + str(StartAngle)

	if(cnt>0):	
		DiffGyroZangle = gyroZangle - StartAngle
		
		#if Diff <0 M2 is faster than 4, speed2 must decrease
		#if Diff>0 M2 is slower than 4, speed2must increase
		if(DiffGyroZangle>DiffThreshold):
			speed2 = speed2 + int(DiffGyroZangle*InverseSlope)
		
		
		
	str_SpeedVsGyro = "speed M2 " +str(speed2)+", speed M4 " +str(speed4)+" DiffGyroZangleDividedBySlope "+ str(int(DiffGyroZangle*InverseSlope))		
	f.write((str_SpeedVsGyro + '\n'))			
		
			
	cnt = cnt + 1	

	
