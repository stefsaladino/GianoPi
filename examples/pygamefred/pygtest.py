import pygame, sys
from pygame.locals import *
fpsClock = pygame.time.Clock()

pygame.init()
pygame.joystick.init()

fps = 24
maxspeed = 56

window = pygame.display.set_mode((640, 480))

pygame.display.set_caption('Joytest')

squirrel = pygame.image.load('squirrel.png')
squix = 320
squiy = 240

# Joystick
try:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print 'joystick is present: ' + joy.get_name()
except pygame.error:
    print 'joystick not found.'

# Main loop
while True:
	window.blit(squirrel, (squix, squiy))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_q:
				pygame.quit()
				sys.exit()
		elif event.type == JOYAXISMOTION:
			x , y = int(joy.get_axis(0)*maxspeed), int(joy.get_axis(1)*maxspeed)
	
	print 'x : ' + str(x) +', and y  '+ str(y)
	
	squix+=x
	squiy+=y
	
	pygame.display.update()
	fpsClock.tick(fps)






