#! /usr/bin/env python
# -*- coding: utf-8 -*- 
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.

#import os
#import pprint
import pygame
import GianoPi
import time
import RPi.GPIO as GPIO
from Adafruit_MotorHAT import Adafruit_MotorHAT

#screen = pygame.display.set_mode((320, 280))
gianopirobot = GianoPi.GianoPi()



class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                    x , y = self.controller.get_axis(0), self.controller.get_axis(1)
                    y = int(y * 127)
                    x = int(x * 127)
           

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
                    time.sleep(0.2)
                    gianopirobot.stop()
  
 
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.
                
                #os.system('clear')
                #pprint.pprint(self.button_data)
                #pprint.pprint(self.axis_data)
                #pprint.pprint(self.hat_data)


#if __name__ == "__main__":
ps4 = PS4Controller()
ps4.init()
ps4.listen()

time.sleep(2.0)

atexit.register(gianopirobot.stop())      # Stop the robot

