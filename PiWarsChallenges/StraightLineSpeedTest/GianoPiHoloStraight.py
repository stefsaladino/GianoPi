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

################################# DC motor test!
maxspeed = 255. #maximum speed divided by sqrt(2)

FL = mh.getMotor(1)
FR = mh.getMotor(2)
RL = mh.getMotor(4)
RR = mh.getMotor(3)

FL.run(Adafruit_MotorHAT.FORWARD) #M1
FR.run(Adafruit_MotorHAT.BACKWARD) #M2
RL.run(Adafruit_MotorHAT.FORWARD) #M4
RR.run(Adafruit_MotorHAT.BACKWARD) #M3


M1_ENA_PIN = 4
#M1_ENB_PIN = 25

M2_ENA_PIN = 22
#M2_ENB_PIN = 5

M3_ENA_PIN = 6
#M3_ENB_PIN = 13

M4_ENA_PIN = 16
#M4_ENB_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(M1_ENA_PIN, GPIO.IN)
GPIO.setup(M2_ENA_PIN, GPIO.IN)
GPIO.setup(M3_ENA_PIN, GPIO.IN)
GPIO.setup(M4_ENA_PIN, GPIO.IN)

global c_M1A, c_M2A, c_M3A, c_M4A
c_M1A = 0.
c_M2A = 0.
c_M3A = 0.
c_M4A = 0.

def increase_c_M1A(channel):
    global c_M1A
    c_M1A += 1.
def increase_c_M2A(channel):
    global c_M2A
    c_M2A += 1.
def increase_c_M3A(channel):
    global c_M3A
    c_M3A += 1.
def increase_c_M4A(channel):
    global c_M4A
    c_M4A += 1.

GPIO.add_event_detect(M1_ENA_PIN, GPIO.RISING, callback=increase_c_M1A)
GPIO.add_event_detect(M2_ENA_PIN, GPIO.RISING, callback=increase_c_M2A)
GPIO.add_event_detect(M3_ENA_PIN, GPIO.RISING, callback=increase_c_M3A)
GPIO.add_event_detect(M4_ENA_PIN, GPIO.RISING, callback=increase_c_M4A)

logfile = 'HoloEncodersA.txt'

FL.setSpeed(int(maxspeed)) #M1
FR.setSpeed(int(maxspeed)) #M2
RL.setSpeed(int(maxspeed)) #M4
RR.setSpeed(int(maxspeed)) #M3

NumSecs = 0.2
	
time.sleep(NumSecs)

data = [c_M1A, c_M2A, c_M3A, c_M4A]
SlowestMotor = min(data)
average_rpm = (c_M1A + c_M2A+c_M3A + c_M4A)/4.
	

str_EnablesA ="Slowest: "+str(SlowestMotor)+", avg: "+str(average_rpm)+", FL: "+str(c_M1A)+", FR: "+str(c_M2A)+", RR: "+str(c_M3A)+", RL: "+str(c_M4A)
f = open(logfile, 'a')
f.write((str_EnablesA + '\n'))			# the value
#f.write((str(datetime.datetime.now())+ '\n'))	# timestamp
f.close()	
	
#NumOfStdErr = 5
#StdErr = 0.1 # as from analysis on plotly - 
Slope = 9.65 #approximation, to be verified

#Intercept = -73
#rpm_from_fit = Intercept + Slope*k
#PourCent = rpm_from_fit*0.05
MaxDiff = Slope
	       
#average_rpm = 346 # depending on the speed, see EncodersA.txt for the actual value, averaged over 4 motors for 1 sec
reference = SlowestMotor
diff_M1A = c_M1A - reference 
diff_M2A = c_M2A - reference
diff_M3A = c_M3A - reference
diff_M4A = c_M4A - reference 

f = open("HoloGoStraight.txt", 'a')
	
if (abs(diff_M1A)  >= MaxDiff) : 
	x_speed1 = maxspeed - diff_M1A/Slope
	x_speed1 = max(0, min(255, x_speed1)) 
	RL.setSpeed(int(x_speed1))
	frase = str(c_M1A) + " - " +str(reference)+ " = " +str(diff_M1A)+", FL at "+str(x_speed1)+","+str(int(x_speed1))	
	f.write(frase+ '\n')

if (abs(diff_M2A)  >= MaxDiff) : 
	x_speed2 = maxspeed - diff_M2A/Slope
	x_speed2 = max(0, min(255, x_speed2)) 
	FL.setSpeed(int(x_speed2))
	frase = str(c_M2A) +" - " +str(reference)+" = " +str(diff_M2A)+", FR at "+str(x_speed2)+","+str(int(x_speed2))
	f.write(frase+ '\n')

if (abs(diff_M3A) >= MaxDiff) : 
	x_speed3 = maxspeed - diff_M3A/Slope
	x_speed3 = max(0, min(255, x_speed3)) 
	FR.setSpeed(int(x_speed3))
	frase = str(c_M3A) +" - " +str(reference)+" = " +str(diff_M3A)+", RR at "+str(x_speed3)+","+str(int(x_speed3))	
	f.write(frase+ '\n')

if (abs(diff_M4A) >= MaxDiff) : 
	x_speed4 = maxspeed - diff_M4A/Slope
	x_speed4 = max(0, min(255, x_speed4)) 
	RR.setSpeed(int(x_speed4))
	frase = str(c_M4A) + " - " +str(reference)+" = " +str(diff_M4A)+", RL at "+str(x_speed4)+","+str(int(x_speed4))
	f.write(frase+ '\n')

f.close()
time.sleep(NumSecs)

while(True):
	
	c_M1A = c_M1A/NumSecs
	c_M2A = c_M2A/NumSecs
	c_M3A = c_M3A/NumSecs
	c_M4A = c_M4A/NumSecs
	
	average_rpm = (c_M1A + c_M2A+c_M3A + c_M4A)/4.
		
	"""
	the following needs to  be done once....
	for each motor the linear fit is:
	y = Intercept + Slope * x 
	so if we know the difference between two y, we know how to change the x
	y1 - y2 = Slope *(x1-x2)
	or diff_Y = Slope*(x1 - x2)
	x1 = x2 + diff_Y/Slope
	"""
	data = [c_M1A, c_M2A, c_M3A, c_M4A]
	SlowestMotor = min(data)

	str_EnablesA ="Slowest: "+str(SlowestMotor)+", avg: "+str(average_rpm)+", FL: "+str(c_M1A)+", FR: "+str(c_M2A)+", RR: "+str(c_M3A)+", RL: "+str(c_M4A)
	f = open(logfile, 'a')
	f.write((str_EnablesA + '\n'))			# the value
	#f.write((str(datetime.datetime.now())+ '\n'))	# timestamp
	f.close()	
		       
	#average_rpm = 346 # depending on the speed, see EncodersA.txt for the actual value, averaged over 4 motors for 1 sec
	reference = SlowestMotor
	diff_M1A = c_M1A - reference 
	diff_M2A = c_M2A - reference
	diff_M3A = c_M3A - reference
	diff_M4A = c_M4A - reference 
	
		
	f = open("HoloGoStraight.txt", 'a')
	
	if (abs(diff_M1A)  >= MaxDiff) : 
		x_speed1 = maxspeed - diff_M1A/Slope
		x_speed1 = max(0, min(255, x_speed1)) 
		RL.setSpeed(int(x_speed1))
		frase = str(c_M1A) + " - " +str(reference)+ " = " +str(diff_M1A)+", FL at "+str(x_speed1)+","+str(int(x_speed1))
		
		f.write(frase+ '\n')

	if (abs(diff_M2A)  >= MaxDiff) : 
		x_speed2 = maxspeed - diff_M2A/Slope
		x_speed2 = max(0, min(255, x_speed2)) 
		FL.setSpeed(int(x_speed2))
		frase = str(c_M2A) +" - " +str(reference)+" = " +str(diff_M2A)+", FR at "+str(x_speed2)+","+str(int(x_speed2))
		f.write(frase+ '\n')

	if (abs(diff_M3A) >= MaxDiff) : 
		x_speed3 = maxspeed - diff_M3A/Slope
		x_speed3 = max(0, min(255, x_speed3)) 
		FR.setSpeed(int(x_speed3))
		frase = str(c_M3A) +" - " +str(reference)+" = " +str(diff_M3A)+", RR at "+str(x_speed3)+","+str(int(x_speed3))
		
		f.write(frase+ '\n')

	if (abs(diff_M4A) >= MaxDiff) : 
		x_speed4 = maxspeed - diff_M4A/Slope
		x_speed4 = max(0, min(255, x_speed4)) 
		RR.setSpeed(int(x_speed4))
		frase = str(c_M4A) + " - " +str(reference)+" = " +str(diff_M4A)+", RL at "+str(x_speed4)+","+str(int(x_speed4))
		
		f.write(frase+ '\n')

	f.close()
	c_M1A = 0.
	c_M2A = 0.
	c_M3A = 0.
	c_M4A = 0.
	time.sleep(NumSecs)