import time
import GianoPi
import pygame
from pygame import locals

#screen = pygame.display.set_mode((320, 280))
pygame.init()
running = 1
gianopirobot = GianoPi.GianoPi()


while running:
    events = pygame.event.get()
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print "LEFT"
                gianopirobot.goleft(250, 0.5)
            if event.key == pygame.K_RIGHT:
                print "RIGHT"
                gianopirobot.goright(250, 0.5)
            if event.key == pygame.K_UP:
                gianopirobot.forward(250, 0.5)
                print "UP"
            if event.key == pygame.K_DOWN:
                print "DOWN"
                gianopirobot.backward(250, 0.5)

time.sleep(2.0)   
gianopirobot.stop()      # Stop the robot
