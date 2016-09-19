#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
SPEED = 150
MOTOR = 3

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
Motor = mh.getMotor(MOTOR)

print "Forward"
Motor.run(Adafruit_MotorHAT.FORWARD);
for i in range(SPEED):
        Motor.setSpeed(SPEED)
        time.sleep(0.01)
                
print "Release"
Motor.run(Adafruit_MotorHAT.RELEASE)
time.sleep(1.0)
        
