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
   


atexit.register(turnOffMotors)

################################# DC motor test!
maxspeed = 255 #maximum speed divided by sqrt(2)

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
#GPIO.add_event_detect(M1_ENA_PIN, GPIO.RISING, callback=increase_c_M1A)
#GPIO.add_event_detect(M2_ENA_PIN, GPIO.RISING, callback=increase_c_M2A)
#GPIO.add_event_detect(M3_ENA_PIN, GPIO.RISING, callback=increase_c_M3A)
#GPIO.add_event_detect(M4_ENA_PIN, GPIO.RISING, callback=increase_c_M4A)

#logfile = 'HoloEncodersA.txt'
NumSecs = 1
speed = 140

#while(True):
FL.setSpeed(int(speed)) #M1
FR.setSpeed(int(speed)) #M2
RL.setSpeed(int(speed)) #M4
RR.setSpeed(int(speed)) #M3
time.sleep(NumSecs)
turnOffMotors()
FL.run(Adafruit_MotorHAT.BACKWARD) #M1
FR.run(Adafruit_MotorHAT.FORWARD) #M2
RL.run(Adafruit_MotorHAT.BACKWARD) #M4
RR.run(Adafruit_MotorHAT.FORWARD) #M3
FL.setSpeed(int(speed)) #M1
FR.setSpeed(int(speed)) #M2
RL.setSpeed(int(speed)) #M4
RR.setSpeed(int(speed)) #M3
time.sleep(NumSecs)
turnOffMotors()

