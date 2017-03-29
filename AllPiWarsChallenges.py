import pygame, os, sys, datetime
from pygame.locals import *
import GianoPi
import atexit
import colorsys
import time
import numpy as np
import colorsys
import time

from blinkt import set_clear_on_exit, set_pixel, show, set_brightness


fpsClock = pygame.time.Clock()

fps = 5

pygame.init()
pygame.joystick.init()

try:
    j = pygame.joystick.Joystick(0)
    j.init()
    print 'joystick is present: ' + j.get_name()
except pygame.error:
    print 'joystick not found.'

buttons = j.get_numbuttons()

ChallengesPython = [ "GoStraightWith2_4.py","2QTR1A_LineFollowing.py", "maze.py", "PS4controller.py", "ArmRC.py"]
ChallengeCounter = 0

gianopirobot = GianoPi.GianoPi()
spacing = 360.0 / 16.0
hue = 0

set_clear_on_exit()
set_brightness(0.1)
flag = True

while (flag):
  for e in pygame.event.get(): # iterate over event stack

    if e.type == pygame.locals.JOYBUTTONDOWN: # 10

      if (j.get_button(13) == 1) : # central pad pressed once - trigger a blinkt blue light on the robot- to be added
				#print 'event : ' + str(e.type) + ' button ' +str(i) +' down : '+ str(j.get_button(i))
        execfile(ChallengesPython(ChallengeCounter))
        ChallengeCounter = ChallengeCounter + 1
        if(ChallengeCounter == 5):
          ChallengeCounter = 0 #  the number of Challenges is 5!
      		 
      elif(j.get_button(12)): # PS logo central button pressed
        gianopirobot.stop()
        flag = False

      elif(j.get_button(9)):
        for t in range (5):
          hue = int(time.time() * 100) % 360
          for x in range(8):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            set_pixel(x,r,g,b)
          show()
          time.sleep(0.001)


  fpsClock.tick(fps)