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
    #GPIO.cleanup()


atexit.register(turnOffMotors)

################################# DC motor test!
maxspeed = 255 #maximum speed divided by sqrt(2)
wheel = 0 #wheel angle
dirrad = 0 #Direction in radians


FL = mh.getMotor(2)
FR = mh.getMotor(3)
RL = mh.getMotor(1)
RR = mh.getMotor(4)

"""
print 'Testing M2 = FL'
FL.setSpeed(int(maxspeed)) #M2
time.sleep(1)
input('Press Enter to continue')
print 'Testing M1 = RL'
RL.setSpeed(int(maxspeed)) #M1
time.sleep(1)
input('Press Enter to continue')
print 'Testing M3 = FR'
FR.setSpeed(int(maxspeed)) #M3
time.sleep(1)
input('Press Enter to continue')
print 'Testing M4 = RR'
RR.setSpeed(int(maxspeed)) #M4
time.sleep(1)
input('Press Enter to continue')
"""

counter = 0
k = 50  	
i = 0

M1_ENA_PIN = 4
#M1_ENB_PIN = 25

M2_ENA_PIN = 22
#M2_ENB_PIN = 5

M3_ENA_PIN = 6
#M3_ENB_PIN = 13

M4_ENA_PIN = 16
#M4_ENB_PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(M1_ENA_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(M2_ENA_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(M3_ENA_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(M4_ENA_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.add_event_detect(M1_ENA_PIN, GPIO.RISING)
GPIO.add_event_detect(M2_ENA_PIN, GPIO.RISING)
GPIO.add_event_detect(M3_ENA_PIN, GPIO.RISING)
GPIO.add_event_detect(M4_ENA_PIN, GPIO.RISING)


global revcount
revcount = 0
def increaserev(channel):
    global revcount
    revcount += 1


logfile = 'EncodersA.txt'
x_speed1 = k
x_speed2 = k
x_speed3 = k
x_speed4 = k

flag = 1

while(k < maxspeed):

#while(True):
    #for i in range (k):
        
        FL.run(Adafruit_MotorHAT.FORWARD) #M2
	FR.run(Adafruit_MotorHAT.BACKWARD) #M3
	RL.run(Adafruit_MotorHAT.FORWARD) #M1
	RR.run(Adafruit_MotorHAT.BACKWARD) #M4
	x_speed1 = k
        x_speed2 = k
        x_speed3 = k
        x_speed4 = k

	FL.setSpeed(max(0, min(maxspeed, int(x_speed2)))) #M2
	RL.setSpeed(max(0, min(maxspeed, int(x_speed1)))) #M1
	FR.setSpeed(max(0, min(maxspeed, int(x_speed3)))) #M3
	RR.setSpeed(max(0, min(maxspeed, int(x_speed4)))) #M4
	#time.sleep(1)
	
	now = time.time()
	AfterOneSec = time.time()
	flag = 1
	
	while (flag==1) :
                c_M1A = 0
                c_M2A = 0
                c_M3A = 0
                c_M4A = 0

                
                now = time.time()
                AfterOneSec = time.time()
                while ((AfterOneSec - now)<=1) :  
                    if GPIO.event_detected(M1_ENA_PIN) :
                        c_M1A = c_M1A+1
                        #time.sleep(0.0001)
                    if GPIO.event_detected(M2_ENA_PIN) :
                        c_M2A = c_M2A+1
                        #time.sleep(0.0001)
                    if GPIO.event_detected(M3_ENA_PIN) :
                        c_M3A = c_M3A+1
                        #time.sleep(0.0001)
                    if GPIO.event_detected(M4_ENA_PIN) :
                        c_M4A = c_M4A+1
                    time.sleep(0.0001)
                        
                    AfterOneSec = time.time()
                                  
                average_rpm = (c_M1A + c_M2A + c_M3A + c_M4A)/4.
		
                """
		the following needs to  be done once....
		For each motor the linear fit is:
		y = Intercept + Slope * x 
		so if we know the difference between two y, we know how to change the x
		 y1 - y2 = Slope *(x1-x2)
		or diff_Y = Slope*(x1 - x2)
		 x1 = x2 + diff_Y/Slope
		"""
		str_EnablesA =str(k)+", "+str(average_rpm)+", "+str(c_M1A)+", "+str(c_M2A)+", "+str(c_M3A)+", "+str(c_M4A)
		f = open(logfile, 'a')
		f.write((str_EnablesA + '\n'))			# the value
		#f.write((str(datetime.datetime.now())+ '\n'))	# timestamp
		f.close()	
		"""
		#NumOfStdErr = 5
		#StdErr = 0.1 # as from analysis on plotly - 
		Slope = 9.5
		#Intercept = -73
		#rpm_from_fit = Intercept + Slope*k
		#PourCent = rpm_from_fit*0.05
		MaxDiff = 10.0
		
		
                
		#average_rpm = 346 # depending on the speed, see EncodersA.txt for the actual value, averaged over 4 motors for 1 sec
		reference = c_M1A
		diff_M1A = c_M1A - reference
		diff_M2A = c_M2A - reference
		diff_M3A = c_M3A - reference
		diff_M4A = c_M4A - reference 
	
		f = open("GoStraight.txt", 'a')
	
		if (abs(diff_M1A ) > MaxDiff) : 
			x_speed1 = k - diff_M1A/Slope
			x_speed1 = max(0, min(255, x_speed1)) 
			RL.setSpeed(int(x_speed1))
			frase = str(c_M1A) + " - " +str(average_rpm)+ " = " +str(diff_M1A)+", speed "+str(k)+", RL at "+str(x_speed1)
			f.write(frase+ '\n')

		if (abs(diff_M2A ) > MaxDiff) : 
			x_speed2 = k - diff_M2A/Slope
			x_speed2 = max(0, min(255, x_speed2)) 
			FL.setSpeed(int(x_speed2))
			frase = str(c_M2A) +" - " +str(average_rpm)+" = " +str(diff_M2A)+", speed "+str(k)+", FL at "+str(x_speed2)
			f.write(frase+ '\n')

		if (abs(diff_M3A ) > MaxDiff) : 
			x_speed3 = k - diff_M3A/Slope
			x_speed3 = max(0, min(255, x_speed3)) 
			FR.setSpeed(int(x_speed3))
			frase = str(c_M3A) +" - " +str(average_rpm)+" = " +str(diff_M3A)+", speed "+str(k)+", FR at "+str(x_speed3)
			f.write(frase+ '\n')

		if (abs(diff_M4A ) > MaxDiff) : 
			x_speed4 = k - diff_M4A/Slope
			x_speed4 = max(0, min(255, x_speed4)) 
			RR.setSpeed(int(x_speed4))
			frase = str(c_M4A) + " - " +str(average_rpm)+" = " +str(diff_M4A)+", speed "+str(k)+", RR at "+str(x_speed4)
			f.write(frase+ '\n')

		f.close()
		"""
                #GPIO.cleanup()
		flag = 0

        k = k + 20
