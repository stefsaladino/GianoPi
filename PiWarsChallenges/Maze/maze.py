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

gianopirobot = GianoPi.GianoPi()

def forwardUntilWall():
	#lala
	while (gianopirobot.get_FrontObjectDistance() > 15):
		gianopirobot.forward(100,104,0.05)
	gianopirobot.stop()

def turnToFreePath():
	#dada
	print "a"

turns = 0
while (turns < 6):
	forwardUntilWall()
	turnToFreePath()
	turns = turns + 1

