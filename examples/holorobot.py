from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
import pygame, sys, datetime
from pygame.locals import *
from math import sqrt, cos, atan2, pi
#import GianoPi
fpsClock = pygame.time.Clock()

fps = 5
maxspeed = 127

pygame.init()
pygame.joystick.init()

#gianopirobot = GianoPi.GianoPi()
# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)
SPEED = 150

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
FL = mh.getMotor(2)
FR = mh.getMotor(3)
RL = mh.getMotor(1)
RR = mh.getMotor(4)

maxspeed = SPEED #maximum speed divided by sqrt(2)
wheel = pi/2 #wheel angle


try:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print 'joystick is present: ' + joy.get_name()
except pygame.error:
    print 'joystick not found.'

# Main loop
while True:
    x,y = int(joy.get_axis(0)), int(joy.get_axis(1))
    dirrad = atan2(x, y) #Direction in radians
    radius = sqrt((x*x)+(y*y))
    c_speed = max(0, min(maxspeed, radius))
    #dirrad = pi/4
    #relative speed of the four wheels
    c_FL = int(-c_speed * cos(wheel - dirrad))
    c_FR = int(c_speed * cos(wheel + dirrad))
    c_RL = int(-c_speed * cos(wheel + dirrad))
    c_RR = int(c_speed * cos(wheel - dirrad))

    #run motors

    if(c_FL>0): FL.run(Adafruit_MotorHAT.FORWARD)
    elif(c_FL<0): FL.run(Adafruit_MotorHAT.BACKWARD)
    #elif(c_FL==0): FL.run(Adafruit_MotorHAT.RELEASE)
    if(c_FR>0): FR.run(Adafruit_MotorHAT.FORWARD)
    elif(c_FR<0): FR.run(Adafruit_MotorHAT.BACKWARD)
    #elif(c_FR==0): FR.run(Adafruit_MotorHAT.RELEASE)
    if(c_RL>0): RL.run(Adafruit_MotorHAT.FORWARD)
    elif(c_RL<0): RL.run(Adafruit_MotorHAT.BACKWARD)
    #elif(c_RL==0): RL.run(Adafruit_MotorHAT.RELEASE)
    if(c_RR>0): RR.run(Adafruit_MotorHAT.FORWARD)
    elif(c_RR<0): RR.run(Adafruit_MotorHAT.BACKWARD)
    #elif(c_RR==0): RR.run(Adafruit_MotorHAT.RELEASE)
 


    FL.setSpeed(abs(c_FL))
    FR.setSpeed(abs(c_FR))
    RL.setSpeed(abs(c_RL))
    RR.setSpeed(abs(c_RR))
    

    #print " FL FR RL RR ", c_FL, c_FR, c_RL, c_RR

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            gianopirobot.stop()
        elif event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
                gianopirobot.stop()
        elif event.type == pygame.locals.JOYBUTTONDOWN:
            pygame.quit()
            sys.exit()
            gianopirobot.stop()

    fpsClock.tick(fps)


# atexit.register(gianopirobot.stop())



