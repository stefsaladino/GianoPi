import pygame
from pygame import locals
import math

pygame.init()

pygame.joystick.init() # main joystick device system

try:
    j = pygame.joystick.Joystick(0) # create a joystick instance
    j.init() # init instance
    print 'Enabled joystick: ' + j.get_name()
except pygame.error:
    print 'no joystick found.'

while 1:
    for e in pygame.event.get(): # iterate over event stack
        if e.type == pygame.locals.JOYAXISMOTION: # 7
            x , y = j.get_axis(0), j.get_axis(1)
            rad = math.atan2(x, y)
            deg = int(rad * 57.2958)
            print 'direction: ' + str(deg) #+' ,x: '+ str(x) + 'y: ' + str(y)