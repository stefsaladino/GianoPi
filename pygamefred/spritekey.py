import pygame, sys, datetime
from pygame.locals import *
fpsClock = pygame.time.Clock()

fps = 30
maxspeed = 56

pygame.init()

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
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			self.rect.y = self.rect.y - 5
		if keys[pygame.K_DOWN]:
			self.rect.y = self.rect.y + 5
		if keys[pygame.K_LEFT]:
			self.rect.x = self.rect.x - 5
		if keys[pygame.K_RIGHT]:
			self.rect.x = self.rect.x + 5
		#print 'pos x : ' + str(self.rect.x) +', pos y  '+ str(self.rect.y) +' time: '+ str(datetime.datetime.now())
		
all_sprites = pygame.sprite.Group()
squirrel = Squirrel()
all_sprites.add(squirrel)

window = pygame.display.set_mode((320, 240))
pygame.display.set_caption('Sprite and Key test')

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






