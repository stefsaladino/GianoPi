import pygame, os, sys, datetime
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from pygame.locals import *


import GianoPi
import atexit
fpsClock = pygame.time.Clock()

fps = 5
maxspeed = 255 #maxspeed divided by sqrt of 2

pygame.init()
pygame.joystick.init()

gianopirobot = GianoPi.GianoPi()



try:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print 'joystick is present: ' + joy.get_name()
except pygame.error:
    print 'joystick not found.'



# Main loop
while True:
    joyx,joyy = int(joy.get_axis(0)*maxspeed), int(joy.get_axis(1)*maxspeed)
    #print 'joyx : ' + str(joyx) +', joyy  '+ str(joyy) +' time: '+ str(datetime.datetime.now())
    if(joyy<0):
        gianopirobot.forward(abs(joyy))
    elif (joyy>0):
        gianopirobot.backward(abs(joyy))
    elif (joyy==0):
        gianopirobot.stop_2_4()
        
    if( joyx >0):
        gianopirobot.goleft(abs(joyx))
    elif(joyx<0):
        gianopirobot.goright(abs(joyx))
    elif(joyx==0):
        gianopirobot.stop_1_3()
        
 

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



