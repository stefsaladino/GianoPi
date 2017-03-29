import pygame, os, sys, datetime
from pygame.locals import *
import GianoPi
import atexit
import colorsys
import time
import numpy as np

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

ChallengesPython = ["examples/GoStraightBlinkt.py", "GoStraightWith2_4.py", 
					"examples/LineBlinkt.py", "2QTR1A_LineFollowing.py", 
					"examples/MazeBlinkt.py", "Maze.py", 
					"examples/PiNoonBlinkt.py", "PS4controller.py", 
					"examples/SkittlesBlinkt.py", "ArmRC.py"]
ChallengeCounter = 0

gianopirobot = GianoPi.GianoPi()

while 1:
    for e in pygame.event.get(): # iterate over event stack
		if e.type == pygame.locals.JOYBUTTONDOWN: # 10
			if (j.get_button(13) == 1) : # central pad pressed once - trigger a blinkt light
				#print 'event : ' + str(e.type) + ' button ' +str(i) +' down : '+ str(j.get_button(i))
				execfile(ChallengesPython(ChallengeCounter))
      		 	ChallengeCounter = ChallengeCounter + 1
      		 	if(ChallengeCounter == 9):
      		 		ChallengeCounter = 0 #  the number of Challenges is 5!
      		 
      		 elif(j.get_numbuttons(12)): # PS logo central button pressed
      		 	execfile("../Pimoroni/blinkt/examples/rainbow.py &")
      		 	gianopirobot.stop()

      		 elif(j.get_numbuttons(9)):
      		 	execfile("../Pimoroni/blinkt/examples/larsen.py &")

    fpsClock.tick(fps)