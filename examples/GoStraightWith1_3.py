# Simple two DC motor robot class usage example..
# Author: Tony DiCola (adapted by Stefania Saladino)
# License: MIT License https://opensource.org/licenses/MIT
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
from math import sqrt, cos, atan2, pi
import RPi.GPIO as GPIO
import datetime
import os, sys
import signal

sys.path.insert(1, os.path.join(sys.path[0], '../..'))
import GianoPi
#######################################################################################################


mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    #GPIO.cleanup()


atexit.register(turnOffMotors)

################################# 
maxspeed = 255 #maximum speed 

MotorOne = mh.getMotor(1)
MotorThree = mh.getMotor(3)

M1_ENA_PIN = 4
#M1_ENB_PIN = 25

M3_ENA_PIN = 6
#M3_ENB_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(M1_ENA_PIN, GPIO.IN)
GPIO.setup(M3_ENA_PIN, GPIO.IN)

global c_M1A, c_M3A
c_M1A = 0
c_M3A = 0

def increase_c_M1A(channel):
    global c_M1A
    c_M1A += 1
def increase_c_M3A(channel):
    global c_M3A
    c_M3A += 1

# to count pulses on the encoders
GPIO.add_event_detect(M1_ENA_PIN, GPIO.RISING, callback=increase_c_M1A)
GPIO.add_event_detect(M3_ENA_PIN, GPIO.RISING, callback=increase_c_M3A)

MotorOne.run(Adafruit_MotorHAT.FORWARD) #M1
MotorThree.run(Adafruit_MotorHAT.BACKWARD) #M4

logfile = 'Encoders1_3.txt' # to keep a record of number of pulses for each motor
x_speed1 = maxspeed
x_speed3 = maxspeed

gianopi = GianoPi.GianoPi()

StopDistance = 20.0
print "Front distance : " +str(gianopi.get_FrontObjectDistance())
vai = 1
#ActualDistance = gianopi.get_FrontObjectDistance()
while (vai) :

		ActualDistance = gianopi.get_FrontObjectDistance()
		#if(ActualDistance>=StopDistance):
		#	print "Front distance : " +str(gianopi.get_FrontObjectDistance())

		#c_M1A = 0
		#c_M3A = 0
	
		#NumSecs = 0.2
		#speedOne = max(0, min(maxspeed, int(x_speed1)))
		#speedThree = max(0, min(maxspeed, int(x_speed3)))
		if(ActualDistance>=StopDistance):
			gianopi.goleft(maxspeed, maxspeed)
		else :
			turnOffMotors()
			vai = 0
		#MotorOne.setSpeed(max(0, min(maxspeed, int(x_speed1)))) #M1
		#MotorThree.setSpeed(max(0, min(maxspeed, int(x_speed3)))) #M3
		#time.sleep(NumSecs)
		"""
		#the slope has nbeen calculated over the number of pulses counted on 1 sec
		temp_c_M1A = c_M1A/NumSecs 
		temp_c_M3A = c_M3A/NumSecs 
		"""
		"""
		the following needs to  be done once.... see SpeedVsENAPulses.py
		for each motor the linear fit is:
		y = Intercept + Slope * x 
		so if we know the difference between two y, we know how to change the x
		y1 - y2 = Slope *(x1-x2)
		or diff_Y = Slope*(x1 - x2)
		x1 = x2 + diff_Y/Slope
		"""
		"""
		str_EnablesA =str(time.time())+ str(maxspeed)+", "+str(temp_c_M1A)+", "+str(temp_c_M3A)
		f = open(logfile, 'a')
		f.write((str_EnablesA + '\n'))			# the value
		#f.write((str(datetime.datetime.now())+ '\n'))	# timestamp
		f.close()	
		"""
		"""
		#StdErr =  from analysis on plotly - 
		m1_Slope = 9.52 #m1
		m3_Slope = 9.78 #m2
	
		#Intercept = from analysis on plotly -
		#rpm_from_fit = Intercept + Slope*k
	
		MaxDiff = 10 # maximum admitted diff between number of pulses (calculated from the error)
		       
		#average_rpm = 346 # depending on the speed, see EncodersA.txt for the actual value, averaged over 4 motors for 1 sec
		reference = min(temp_c_M1A, temp_c_M3A) # the one which go faster is the one that can be slowed down..., so the reference is the slowest!
		diff_M1A = temp_c_M1A - reference
		diff_M3A = temp_c_M3A - reference
	

		#f = open("GoStraight1_3.txt", 'a')
	
		if (diff_M1A  >= MaxDiff) : 
			x_speed1 = maxspeed - diff_M1A/m1_Slope
			x_speed1 = max(0, min(255, x_speed1)) 
			#MotorOne.setSpeed(int(x_speed1))

			#frase = str(time.time())+"M1 "+str(temp_c_M1A) +" - M3 " +str(reference)+" = " +str(diff_M1A)+", speed "+str(maxspeed)+", M1 set at "+str(x_speed1)
			#f.write(frase+ '\n')

		if (diff_M3A >= MaxDiff) : 
			x_speed3 = maxspeed - diff_M3A/m3_Slope
			x_speed3 = max(0, min(255, x_speed3)) 
			#MotorThree.setSpeed(int(x_speed3))
			#frase = str(time.time())+"M3 "+str(temp_c_M3A) +" - M1 " +str(reference)+" = " +str(diff_M3A)+", speed "+str(maxspeed)+", M3 set at "+str(x_speed3)
			#f.write(frase+ '\n')
		"""
		#f.close()
		#else :
		#	turnOffMotors()
		#	vai = 0
	
