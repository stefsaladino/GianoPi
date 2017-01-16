import pygame
from pygame import locals
import argparse
from math import pi, atan2, cos, sqrt

parser = argparse.ArgumentParser(description='x and y.')

parser.add_argument('x', type=float, help='integer value for x')
parser.add_argument('y', type=float, help='integer value for y')

args = parser.parse_args()
x = args.x
y = args.y
#pi = math.pi

maxspeed = 127 #maximum speed

wheel = pi/4 #wheel angle

c = (sqrt((x*x)+(y*y)))*(maxspeed/sqrt(2)) #speed

#pygame.init()

'''pygame.joystick.init() # main joystick device system

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
            print 'direction: ' + str(rad) #+' ,x: '+ str(x) + 'y: ' + str(y)'''

dirrad = atan2(x, y) #Direction in radians
dirdeg = int(dirrad * 57.2958) #direction in degrees

#relative speed of the four wheels
c_FL = int(maxspeed * cos(wheel + dirrad))
c_FR = int(-maxspeed * cos(wheel - dirrad))
c_RL = int(maxspeed * cos(wheel - dirrad))
c_RR = int(-maxspeed * cos(wheel + dirrad))

print 'direction: ' + str(dirrad) +'rad / ' + str(dirdeg) + 'deg, x: '+ str(x) + ', y: ' + str(y)
print 'c: ' + str(c)
print 'c_FL: ' + str(c_FL)
print 'c_FR: ' + str(c_FR)
print 'r_RL: ' + str(c_RL)
print 'r_RR: ' + str(c_RR)