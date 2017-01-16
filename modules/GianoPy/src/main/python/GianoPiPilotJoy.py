import pygame, sys, datetime
from pygame.locals import *
import GianoPi
fpsClock = pygame.time.Clock()

fps = 5
maxspeed = 127

pygame.init()
pygame.joystick.init()

gianopirobot = GianoPi.GianoPi()

try:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print 'joystick is present: ' + joy.get_name()
except pygame.error:
    print 'joystick not found.'

#window = pygame.display.set_mode((320, 240))
#pygame.display.set_caption('Sprite and Joy test')

# Main loop
while True:
    joyx,joyy = int(joy.get_axis(0)*maxspeed), int(joy.get_axis(1)*maxspeed)
    #print 'joyx : ' + str(joyx) +', joyy  '+ str(joyy) +' time: '+ str(datetime.datetime.now())
    gianopirobot.forward(abs(joyy), 0.18)

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






