import time
import GianoPi
import pygame
from pygame import locals

import RPi.GPIO as GPIO

from Adafruit_MotorHAT import Adafruit_MotorHAT

#screen = pygame.display.set_mode((320, 280))
pygame.init()
running = 1
gianopirobot = GianoPi.GianoPi()

pygame.joystick.init()

try:
    j = pygame.joystick.Joystick(0) # create a joystick instance
    j.init() # init instance
    print 'Enabled joystick: ' + j.get_name()
except pygame.error:
    print 'no joystick found.'
    
while running:
    events = pygame.event.get()
    
    for event in events:
        #print 'event : ' + str(event.type)
        if event.type == pygame.locals.JOYAXISMOTION: # 7
            x , y = j.get_axis(0), j.get_axis(1)
            y = int(y * 127)
            x = int(x * 127)
            print 'x and y : ' + str(x) +' , '+ str(y)

            gianopirobot._m1_speed(abs(x))
            gianopirobot._m3_speed(abs(x))
            gianopirobot._m2_speed(abs(y))
            gianopirobot._m4_speed(abs(y))

            if (y < 0):
                gianopirobot._m2.run(Adafruit_MotorHAT.BACKWARD)
                gianopirobot._m4.run(Adafruit_MotorHAT.FORWARD)
            elif (y > 0):
                gianopirobot._m2.run(Adafruit_MotorHAT.FORWARD)
                gianopirobot._m4.run(Adafruit_MotorHAT.BACKWARD)
            if (x < 0):
                gianopirobot._m1.run(Adafruit_MotorHAT.FORWARD)
                gianopirobot._m3.run(Adafruit_MotorHAT.FORWARD)
            elif (x > 0):
                gianopirobot._m1.run(Adafruit_MotorHAT.BACKWARD)
                gianopirobot._m3.run(Adafruit_MotorHAT.BACKWARD)
            #time.sleep(0.2) 

time.sleep(2.0)   
gianopirobot.stop()      # Stop the robot
