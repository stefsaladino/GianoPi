# Simple two DC motor robot class usage example..
# Author: Tony DiCola (adapted by Stefania Saladino)
# License: MIT License https://opensource.org/licenses/MIT
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
from math import sqrt, cos, atan2, pi
import RPi.GPIO as GPIO
import datetime
import sys
import signal

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
maxspeed = 255 #maximum speed 

MotorTwo = mh.getMotor(2)
MotorFour = mh.getMotor(4)

M2_ENA_PIN = 22

M4_ENA_PIN = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(M2_ENA_PIN, GPIO.IN)
GPIO.setup(M4_ENA_PIN, GPIO.IN)

global c_M2A, c_M4A
c_M2A = 0
c_M4A = 0

def increase_c_M2A(channel):
    global c_M2A
    c_M2A += 1
def increase_c_M4A(channel):
    global c_M4A
    c_M4A += 1

# to count pulses on the encoders
GPIO.add_event_detect(M2_ENA_PIN, GPIO.RISING, callback=increase_c_M2A)
GPIO.add_event_detect(M4_ENA_PIN, GPIO.RISING, callback=increase_c_M4A)

MotorTwo.run(Adafruit_MotorHAT.FORWARD) #M1
MotorFour.run(Adafruit_MotorHAT.BACKWARD) #M4

logfile = 'Encoders2_4.txt' # to keep a record of number of pulses for each motor
x_speed2 = maxspeed
x_speed4 = maxspeed

while(True) :

	c_M2A = 0
	c_M4A = 0
	
	NumSecs = 0.5

	MotorTwo.setSpeed(max(0, min(maxspeed, int(x_speed2)))) #M1
	MotorFour.setSpeed(max(0, min(maxspeed, int(x_speed4)))) #M3
	time.sleep(NumSecs)
	
	#the slope has nbeen calculated over the number of pulses counted on 1 sec
	temp_c_M2A = c_M2A/NumSecs 
	temp_c_M4A = c_M4A/NumSecs 
		
	"""
	the following needs to  be done once.... see SpeedVsENAPulses.py
	for each motor the linear fit is:
	y = Intercept + Slope * x 
	so if we know the difference between two y, we know how to change the x
	y1 - y2 = Slope *(x1-x2)
	or diff_Y = Slope*(x1 - x2)
	x1 = x2 + diff_Y/Slope
	"""
	
	str_EnablesA =str(time.time())+ str(maxspeed)+", "+str(temp_c_M2A)+", "+str(temp_c_M4A)
	f = open(logfile, 'a')
	f.write((str_EnablesA + '\n'))			# the value
	#f.write((str(datetime.datetime.now())+ '\n'))	# timestamp
	f.close()	
		
	
	#StdErr =  from analysis on plotly - 
	m2_Slope = 9.5 #guess
	m4_Slope = 9.5 #guess
	
	#Intercept = from analysis on plotly -
	#rpm_from_fit = Intercept + Slope*k
	
	MaxDiff = 1 # maximum admitted diff between number of pulses (calculated from the error)
		       
	#average_rpm = 346 # depending on the speed, see EncodersA.txt for the actual value, averaged over 4 motors for 1 sec
	reference = min(temp_c_M2A, temp_c_M4A) # the one which go faster is the one that can be slowed down..., so the reference is the slowest!
	diff_M2A = temp_c_M2A - reference
	diff_M4A = temp_c_M4A - reference
	

	f = open("GoStraight2_4.txt", 'a')
	
	if (diff_M2A  >= MaxDiff) : 
		x_speed2 = maxspeed - diff_M2A/m2_Slope
		x_speed2 = max(0, min(255, x_speed2)) 
		MotorTwo.setSpeed(int(x_speed2))

		frase = str(time.time())+"M2 "+str(temp_c_M2A) +" - M4 " +str(reference)+" = " +str(diff_M2A)+", speed "+str(maxspeed)+", M2 set at "+str(x_speed2)
		f.write(frase+ '\n')

	if (diff_M4A >= MaxDiff) : 
		x_speed4 = maxspeed - diff_M4A/m4_Slope
		x_speed4 = max(0, min(255, x_speed4)) 
		MotorFour.setSpeed(int(x_speed4))
		frase = str(time.time())+"M4 "+str(temp_c_M4A) +" - M2 " +str(reference)+" = " +str(diff_M4A)+", speed "+str(maxspeed)+", M4 set at "+str(x_speed4)
		f.write(frase+ '\n')


	f.close()

	
