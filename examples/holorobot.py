
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
import pygame, sys, os, datetime
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from pygame.locals import *
from math import sqrt, cos, atan2, pi
import GianoPi

fpsClock = pygame.time.Clock()

fps = 5
maxspeed = 255

pygame.init()
pygame.joystick.init()
running = 1
gianopirobot = GianoPi.GianoPi()

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

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
FL.run(Adafruit_MotorHAT.FORWARD)
RL.run(Adafruit_MotorHAT.FORWARD)
FR.run(Adafruit_MotorHAT.BACKWARD)
RR.run(Adafruit_MotorHAT.BACKWARD)

maxspeed = 255 #maximum speed divided by sqrt(2)
wheel = pi/4 #wheel angle
fps = 5

try:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print 'joystick is present: ' + joy.get_name()
except pygame.error:
    print 'joystick not found.'
    
fpsClock = pygame.time.Clock()

# Main loop
while running:

    x,y = int(joy.get_axis(0)), int(joy.get_axis(1))
    
    dirrad = atan2(x, y) #Direction in radians
    radius = sqrt((x*x)+(y*y))
    c_speed = maxspeed*radius
    c_FL = int(-c_speed * cos(wheel - dirrad))
    c_FR = int(c_speed * cos(wheel + dirrad))
    c_RL = int(-c_speed * cos(wheel + dirrad))
    c_RR = int(c_speed * cos(wheel - dirrad))

    if(c_FL>0): FL.run(Adafruit_MotorHAT.FORWARD)
    elif(c_FL<0): FL.run(Adafruit_MotorHAT.BACKWARD)
    elif(c_FL==0): FL.run(Adafruit_MotorHAT.RELEASE)
    if(c_FR>0): FR.run(Adafruit_MotorHAT.BACKWARD)
    elif(c_FR<0): FR.run(Adafruit_MotorHAT.FORWARD)
    elif(c_FR==0): FR.run(Adafruit_MotorHAT.RELEASE)
    if(c_RL>0): RL.run(Adafruit_MotorHAT.FORWARD)
    elif(c_RL<0): RL.run(Adafruit_MotorHAT.BACKWARD)
    elif(c_RL==0): RL.run(Adafruit_MotorHAT.RELEASE)
    if(c_RR>0): RR.run(Adafruit_MotorHAT.BACKWARD)
    elif(c_RR<0): RR.run(Adafruit_MotorHAT.FORWARD)
    elif(c_RR==0): RR.run(Adafruit_MotorHAT.RELEASE)
    #run motors
        
    FL.setSpeed(abs(c_FL))
    FR.setSpeed(abs(c_FR))
    RL.setSpeed(abs(c_RL))
    RR.setSpeed(abs(c_RR))
 

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

    #pygame.display.update()
    fpsClock.tick(fps)


atexit.register(gianopirobot.stop())

   
            
"""             
f = open("JoyHolo.txt", 'a')
str_joy = str(x)+", "+str(y)+", "+str(c_FL) + ", "+str(c_RL) + ", "+str(c_FR) + ", "+str(c_RR)
f.write((str_joy + '\n'))          # the value
f.close()   
"""    




