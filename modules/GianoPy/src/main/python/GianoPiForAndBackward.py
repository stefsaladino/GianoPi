# Simple two DC motor robot class usage example.
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
""""jhjhjhjhj
def printusage(progname):
        print progname + ' <gpio-pin-number> <filename> [debug]'
        print 'Example usage: ' 
	print progname + ' 23 /path/to/mylogfile'
        print progname + ' 23 /path/to/mylogfile debug'
	sys.exit(-1)


def signal_handler(signal, frame):
        if verbose:
		print('You pressed Ctrl+C, so exiting')
	GPIO.cleanup()
        sys.exit(0)


def readvalue(myworkfile):
	try:
		f = open(myworkfile, 'ab+')		# open for reading. If it does not exist, create it
		value = int(f.readline().rstrip())	# read the first line; it should be an integer value
	except:
		value = 0				# if something went wrong, reset to 0
	#print "old value is", value
	f.close()	# close for reading
	return value


def writevalue(myworkfile,value):
	f = open(myworkfile, 'w')
	f.write((str(value)+ '\n'))			# the value
	f.write((str(datetime.datetime.now())+ '\n'))	# timestamp
	f.close()	
"""
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
k = 160  	
i = 0

M1_ENA_PIN = 4
M1_ENB_PIN = 25

M2_ENA_PIN = 22
M2_ENB_PIN = 5

M3_ENA_PIN = 6
M3_ENB_PIN = 13

M4_ENA_PIN = 16
M4_ENB_PIN = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(M1_ENA_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(M1_ENB_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.setup(M2_ENA_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(M2_ENB_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.setup(M3_ENA_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(M3_ENB_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

GPIO.setup(M4_ENA_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(M4_ENB_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


logfile = 'EncodersA.txt'
x_speed1 = k
x_speed2 = k
x_speed3 = k
x_speed4 = k

flag = 1
#while(k < maxspeed):

while(True): 

	c_M1A = 0
	c_M2A = 0
	c_M3A = 0
	c_M4A = 0

	#for i in range (k):
	FL.run(Adafruit_MotorHAT.FORWARD) #M2
	FR.run(Adafruit_MotorHAT.BACKWARD) #M3
	RL.run(Adafruit_MotorHAT.FORWARD) #M1
	RR.run(Adafruit_MotorHAT.BACKWARD) #M4
	
	FL.setSpeed(int(x_speed2)) #M2
	RL.setSpeed(int(x_speed1)) #M1
	FR.setSpeed(int(x_speed3)) #M3
	RR.setSpeed(int(x_speed4)) #M4
	#time.sleep(1)
	
	now = time.time()
	AfterOneSec = time.time()
	flag = 1
	while (flag==1) :

		while ((AfterOneSec - now)<=1) :
			GPIO.wait_for_edge(M1_ENA_PIN, GPIO.RISING)
			c_M1A = c_M1A + 1	
			GPIO.wait_for_edge(M1_ENA_PIN, GPIO.FALLING)
	
			GPIO.wait_for_edge(M2_ENA_PIN, GPIO.RISING)
			c_M2A = c_M2A + 1	
			GPIO.wait_for_edge(M2_ENA_PIN, GPIO.FALLING)
			
			GPIO.wait_for_edge(M3_ENA_PIN, GPIO.RISING)
			c_M3A = c_M3A + 1	
			GPIO.wait_for_edge(M3_ENA_PIN, GPIO.FALLING)

			GPIO.wait_for_edge(M4_ENA_PIN, GPIO.RISING)
			c_M4A = c_M4A + 1	
			GPIO.wait_for_edge(M4_ENA_PIN, GPIO.FALLING)
		
			AfterOneSec = time.time()
	
		average_rpm = (c_M1A+c_M2A+c_M3A+c_M4A)/4.0

		"""
		the following has alrady been done once....
		 and the linear fit is: y = 38.2 + 2.1 * x , stderr = 0.1
		so if we know the difference between two y, we know how to change the x
		 y1 - y2 = 2.1 *(x1-x2)
		or diff_Y = 2.1*(x1 - x2)
		 x1 = x2 + diff_Y/2.1
		"""
		str_EnablesA = str(k) + ", " + str(average_rpm) +", "+str(c_M1A) +", "+str(c_M2A)+", "+str(c_M3A)+", "+str(c_M4A)
		f = open(logfile, 'a')
		f.write((str_EnablesA + '\n'))			# the value
		f.write((str(datetime.datetime.now())+ '\n'))	# timestamp
		f.close()	
		
	
		#NumOfStdErr = 5
		#StdErr = 0.1 # as from analysis on plotly - use SpeedVsENAPulses.py to compute
		Slope = 2.1
		#Intercept = 38.2
		#rpm_from_fit = Intercept + Slope*k
		#PourCent = rpm_from_fit*0.05
		MaxDiff = 1.0
	
		"""
		diff_M1A = c_M1A - rpm_from_fit
		diff_M2A = c_M2A - rpm_from_fit
		diff_M3A = c_M3A - rpm_from_fit
		diff_M4A = c_M4A - rpm_from_fit 
		"""
		#verage_rpm = 346 # depending on the speed, see EncodersA.txt for the actual value, averaged over 4 motors for 1 sec
		diff_M1A = c_M1A - average_rpm
		diff_M2A = c_M2A - average_rpm
		diff_M3A = c_M3A - average_rpm
		diff_M4A = c_M4A - average_rpm 
	
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

		flag = 0

	#k = k + 20

	