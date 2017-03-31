import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
import pygame, os, sys, datetime
import RPi.GPIO as GPIO
import signal
import smbus
import math

from blinkt import set_clear_on_exit, set_pixel, show, set_brightness

sys.path.insert(1, os.path.join(sys.path[0], '../..'))
import GianoPi


gianopirobot = GianoPi.GianoPi()


speed2 = 100 #motor 2 is slower by 10sh
speed4 = 90
speed1 = 100
speed3 =100
turnspeed = 50
maxdistance = 10
mindistance = 5
secondwall = 20
WRONG = 100

def forwardUntilWall():
	#lala
	while (gianopirobot.get_FrontObjectDistance() > 15):
		gianopirobot.forward(100,106,0.05)
	gianopirobot.stop()

def keepDistanceFromWallFor(dis):
	#meas_distance = gianopirobot.get_rightobjectdistance()
	
		if((dis>=mindistance)&(dis<=maxdistance)): # robot at correct distance from wall
			gianopirobot.forward(speed2,speed4,0.02)
			time.sleep(0.02)

		elif((dis>maxdistance)&(dis<=secondwall)): #robot too far from wall
			gianopirobot.turnrightall(turnspeed, 0.001)
			time.sleep(0.001)
			gianopirobot.forward(speed2,speed4,0.01)
			time.sleep(0.01)

		elif(dis<mindistance): #robot too close to wall
			gianopirobot.turnleftall(turnspeed, 0.001)
			time.sleep(0.001)
			gianopirobot.forward(speed2,speed4,0.01)
			time.sleep(0.01)
	
def middlePart(dis):
	#meas_distance = gianopirobot.get_rightobjectdistance()
		
		if((dis>=mindistance)&(dis<=maxdistance)): # robot at correct distance from wall
			gianopirobot.backward(speed2,speed4,0.02)
			time.sleep(0.02)

		elif((dis>maxdistance)&(dis<=secondwall)): #robot too far from wall
			gianopirobot.turnleftall(turnspeed, 0.001)
			time.sleep(0.001)
			gianopirobot.backward(speed2,speed4,0.01)
			time.sleep(0.01)

		elif(dis<mindistance): #robot too close to wall
			gianopirobot.turnrightall(turnspeed, 0.001)
			time.sleep(0.001)
			gianopirobot.backward(speed2,speed4,0.01)
			time.sleep(0.01)
	




#for lednum in range (8):
#	set_pixel(lednum, 0, 0, 255)
#show()
set_clear_on_exit()

atexit.register(gianopirobot.stop())	

turns = 0

while (True):
	
	if(gianopirobot.get_rightobjectdistance()<secondwall):
		keepDistanceFromWallFor(gianopirobot.get_rightobjectdistance())
		time.sleep(0.03) #the time needed to measure the distance
	else:
		gianopirobot.forward(speed2, speed4, 0.5)
		time.sleep(0.1)
		while(gianopirobot.get_rightobjectdistance()>mindistance):
			gianopirobot.goright(speed1,speed3,0.02)
			time.sleep(0.03)
		#gianopirobot.stop()

		if(gianopirobot.get_rightobjectdistance()<secondwall):
			middlePart(gianopirobot.get_rightobjectdistance())	#robot will fall the wall backward	
			time.sleep(0.03)
		else:
			gianopirobot.backward(speed2, speed4, 0.02)
			time.sleep(0.02)

			while(gianopirobot.get_rightobjectdistance()>mindistance):
				
				gianopirobot.goright(speed1,speed3,0.02)
				time.sleep(0.03)
