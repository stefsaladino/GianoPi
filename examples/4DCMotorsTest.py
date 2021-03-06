#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
SPEED = 100


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
MotorOne = mh.getMotor(1)
MotorTwo = mh.getMotor(2)
MotorThree = mh.getMotor(3)
MotorFour = mh.getMotor(4)

# set the speed to start, from 0 (off) to 255 (max speed)
#MotorOne.setSpeed(SPEED)
#MotorOne.run(Adafruit_MotorHAT.FORWARD);
# turn on motor
#MotorOne.run(Adafruit_MotorHAT.RELEASE);

#while(True):
print "Forward 1&3! "
MotorOne.run(Adafruit_MotorHAT.FORWARD);
MotorThree.run(Adafruit_MotorHAT.BACKWARD);
for i in range(SPEED):
        MotorOne.setSpeed(SPEED)
        MotorThree.setSpeed(SPEED)
        time.sleep(0.01)
                
print "Backward 1&3! "
MotorOne.run(Adafruit_MotorHAT.BACKWARD)
MotorThree.run(Adafruit_MotorHAT.FORWARD);
for i in range(SPEED):
        MotorOne.setSpeed(SPEED)
        MotorThree.setSpeed(SPEED) 
        time.sleep(0.01)

print "Release 1&3"
MotorOne.run(Adafruit_MotorHAT.RELEASE)
MotorThree.run(Adafruit_MotorHAT.RELEASE)
#time.sleep(1.0)
        
print "Forward 2&4! "
MotorTwo.run(Adafruit_MotorHAT.FORWARD);
MotorFour.run(Adafruit_MotorHAT.BACKWARD);
for i in range(SPEED):
        MotorTwo.setSpeed(SPEED)
        MotorFour.setSpeed(SPEED)
        time.sleep(0.01)
                
print "Backward 2&4! "
MotorTwo.run(Adafruit_MotorHAT.BACKWARD)
MotorFour.run(Adafruit_MotorHAT.FORWARD);
for i in range(SPEED):
        MotorTwo.setSpeed(SPEED)
        MotorFour.setSpeed(SPEED) 
        time.sleep(0.01)

print "Release 2&4"
MotorTwo.run(Adafruit_MotorHAT.RELEASE)
MotorFour.run(Adafruit_MotorHAT.RELEASE)
#time.sleep(1.0)


