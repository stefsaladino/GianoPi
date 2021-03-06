import pygame, sys, datetime
from pygame.locals import *
fpsClock = pygame.time.Clock()

fps = 30
maxspeed = 8

pygame.init()
pygame.joystick.init()

try:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print 'joystick is present: ' + joy.get_name()
except pygame.error:
    print 'joystick not found.'

class Squirrel(pygame.sprite.Sprite):
    image = pygame.image.load('squirrel.png')
    def __init__(self):
    	pygame.sprite.Sprite.__init__(self) 
    	self.image = Squirrel.image 
    	#self.image = pygame.Surface((50, 50))
    	#self.image.fill((255, 0, 0))
    	self.rect = self.image.get_rect()
    	self.rect.center = (160, 120)
    def update(self):
    	joyx , joyy = int(joy.get_axis(0)*maxspeed), int(joy.get_axis(1)*maxspeed)
    	self.rect.x = self.rect.x+joyx
    	self.rect.y = self.rect.y+joyy
        if self.rect.x > 320:
            self.rect.x = 0
        if self.rect.x <  0:
            self.rect.x = 320
        if self.rect.y > 240:
            self.rect.y = 0
        if self.rect.y <  0:
            self.rect.y = 2400
    	#print 'joyx : ' + str(joyx) +', joyy  '+ str(joyy) +' time: '+ str(datetime.datetime.now())
    	

all_sprites = pygame.sprite.Group()
squirrel = Squirrel()
all_sprites.add(squirrel)

window = pygame.display.set_mode((320, 240))
pygame.display.set_caption('Sprite and Joy test')

# Main loop
while True:
	all_sprites.update()
	window.fill((0, 0, 0))
	all_sprites.draw(window)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_q:
				pygame.quit()
				sys.exit()

	pygame.display.update()
	fpsClock.tick(fps)






