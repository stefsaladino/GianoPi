import pygame
from pygame import locals

pygame.init()

pygame.joystick.init() # main joystick device system
fpsClock = pygame.time.Clock()

fps = 5
hat_data = None

try:
    j = pygame.joystick.Joystick(0) # create a joystick instance
    j.init() # init instance
    print 'Enabled joystick : ' + j.get_name()
    print 'ID : '+str(j.get_id())
    print 'number of hat controls : '+str(j.get_numhats())
    print 'number of buttons : '+ str(j.get_numbuttons())
    print 'number of trackballs : '+str(j.get_numballs())
    print 'number of axes : ' +str(j.get_numaxes())
except pygame.error:
    print 'no joystick found.'
    
buttons = j.get_numbuttons()

while 1:
    for e in pygame.event.get(): # iterate over event stack
        #print 'event : ' + str(e.type)

        
        for i in range(buttons) :
            if(j.get_button(i) == 1):
        #if e.type == pygame.locals.JOYAXISMOTION: # 7
        #    x , y = j.get_axis(0), j.get_axis(1)
        #    print 'x and y : ' + str(x) +' , '+ str(y)
                print ' current state of button ' +str(i) +' : '+ str(j.get_button(i))
        
        if e.type == pygame.locals.JOYHATMOTION: # 9
            print 'event : ' +str(e.type) + ' hat motion : ' + str(e.value)

        elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
            for i in range(buttons) :
                if (j.get_button(i) == 1) :
                    print 'event : ' + str(e.type) + ' button ' +str(i) +' down : '+ str(j.get_button(i))
        elif e.type == pygame.locals.JOYBUTTONUP: # 11
            for i in range(buttons) :
                if (j.get_button(i) == 1) :
                    print 'event : ' + str(e.type) + ' button ' +str(i) +' up : '+ str(j.get_button(i))
        

    fpsClock.tick(fps)