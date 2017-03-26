import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
import pygame, os, sys, datetime
import RPi.GPIO as GPIO
import signal
import smbus
import math

sys.path.insert(1, os.path.join(sys.path[0], '../BerryIMU/python-BerryIMU-gryo-accel-compass'))
from LSM9DS0 import *

bus = smbus.SMBus(1)

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
SPEED = 200

def writeACC(register,value):
        bus.write_byte_data(ACC_ADDRESS , register, value)
        return -1

def writeGRY(register,value):
        bus.write_byte_data(GYR_ADDRESS, register, value)
        return -1

def writeMAG(register,value):
        bus.write_byte_data(MAG_ADDRESS, register, value)
        return -1

def readACCx():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_X_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_X_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCy():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Y_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Y_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readACCz():
        acc_l = bus.read_byte_data(ACC_ADDRESS, OUT_Z_L_A)
        acc_h = bus.read_byte_data(ACC_ADDRESS, OUT_Z_H_A)
	acc_combined = (acc_l | acc_h <<8)

	return acc_combined  if acc_combined < 32768 else acc_combined - 65536


def readGYRz():
        gyr_l = bus.read_byte_data(GYR_ADDRESS, OUT_Z_L_G)
        gyr_h = bus.read_byte_data(GYR_ADDRESS, OUT_Z_H_G)
        gyr_combined = (gyr_l | gyr_h <<8)

        return gyr_combined  if gyr_combined < 32768 else gyr_combined - 65536
def readMAGx():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_X_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_X_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGy():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Y_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Y_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536


def readMAGz():
        mag_l = bus.read_byte_data(MAG_ADDRESS, OUT_Z_L_M)
        mag_h = bus.read_byte_data(MAG_ADDRESS, OUT_Z_H_M)
        mag_combined = (mag_l | mag_h <<8)

        return mag_combined  if mag_combined < 32768 else mag_combined - 65536

mh = Adafruit_MotorHAT(addr=0x60)
# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# 
#initialise the gyroscope
writeGRY(CTRL_REG1_G, 0b00001111) #Normal power mode, all axes enabled
writeGRY(CTRL_REG4_G, 0b00110000) #Continuos update, 2000 dps full scale
################################# 


#initialise the magnetometer
writeMAG(CTRL_REG5_XM, 0b11110000) #Temp enable, M data rate = 50Hz
writeMAG(CTRL_REG6_XM, 0b01100000) #+/-12gauss
writeMAG(CTRL_REG7_XM, 0b00000000) #Continuous-conversion mode

#initialise the accelerometer
writeACC(CTRL_REG1_XM, 0b01100111) #z,y,x axis enabled, continuos update,  100Hz data rate
writeACC(CTRL_REG2_XM, 0b00100000) #+/- 16G full scale


MotorTwo = mh.getMotor(2)
MotorFour = mh.getMotor(4)

# set the speed to start, from 0 (off) to SPEED (max speed)
#MotorOne.setSpeed(SPEED)
atexit.register(turnOffMotors)

cnt = 0

while(True):
	
	#Read the accelerometer,gyroscope and magnetometer values
	ACCx = readACCx()
	ACCy = readACCy()
	ACCz = readACCz()
	#GYRx = readGYRx()
	#GYRy = readGYRy()
	GYRz = readGYRz()
	MAGx = readMAGx()
	MAGy = readMAGy()
	MAGz = readMAGz()
	##Convert Accelerometer values to degrees
	AccXangle =  (math.atan2(ACCy,ACCz)+M_PI)*RAD_TO_DEG
	AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG
	
	
	####################################################################
	######################Correct rotation value########################
	####################################################################
	#Change the rotation value of the accelerometer to -/+ 180 and
    	#move the Y axis '0' point to up.
    	#
    	#Two different pieces of code are used depending on how your IMU is mounted.
	#If IMU is up the correct way, Skull logo is facing down, Use these lines
	AccXangle -= 180.0
	if AccYangle > 90:
		AccYangle -= 270.0
	else:
		AccYangle += 90.0

	#Normalize accelerometer raw values.
	accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
	accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
	
	####################################################################
	###################Calculate pitch and roll#########################
	####################################################################
	#Use these two lines when the IMU is up the right way. Skull logo is facing down
	pitch = math.asin(accXnorm)
	roll = -math.asin(accYnorm/math.cos(pitch))
	

	#Calculate the new tilt compensated values
	magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
	magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)

	#Calculate tilt compensated heading
        tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/M_PI

        if tiltCompensatedHeading < 0:
                tiltCompensatedHeading += 360

	#Convert Gyro raw to degrees per second	
	rate_gyr_z =  GYRz * G_GAIN

	
	#Calculate heading
	heading = 180 * math.atan2(MAGy,MAGx)/M_PI

	#Only have our heading between 0 and 360
	if heading < 0:
	 	heading += 360

	
	MotorTwo.run(Adafruit_MotorHAT.BACKWARD)
	MotorFour.run(Adafruit_MotorHAT.FORWARD)
	#MotorTwo.setSpeed(SPEED)
	#MotorFour.setSpeed(SPEED+2) # Motor Four is slower than motor 2
	#time.sleep(0.01)

	
	if (cnt>0):
		diffheading = heading-PastHeading
		if (abs(diffheading)>= 0.8):
			if(diffheading > 0):
				MotorTwo.setSpeed(SPEED+12)
			if (diffheading < 0):
				MotorFour.setSpeed(SPEED+16)
			
			print "rate_GZ " + str(rate_gyr_z)+" HEADING  "+ str(heading) + " diff " +str(diffheading)
		else:
			MotorTwo.setSpeed(SPEED)
			MotorFour.setSpeed(SPEED+4)
		time.sleep(0.01)

	PastHeading = heading

	cnt = cnt + 1

	