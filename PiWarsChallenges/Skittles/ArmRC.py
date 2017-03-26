#!/usr/bin/env python
from __future__ import division, print_function
import pygame, datetime, sys, os
from pygame.locals import *
import atexit
from time import sleep
from pyxl320 import ServoSerial
from pyxl320 import Packet, xl320

sys.path.insert(1, os.path.join(sys.path[0], '../..'))
import GianoPi
gianopirobot = GianoPi.GianoPi()



# pygame
fpsClock = pygame.time.Clock()

fps = 10
pygame.init()
pygame.joystick.init()

# Arm
m_ID = 1
port = '/dev/ttyUSB0'
sleep_time = 0.1
servospeed = 0.5
start_angle = 150.0
angle = 150.
maxspeed = 255 #maxspeed of dc motors
led_color = 2
NumMotors = 6
motorFlag = 0

serial = ServoSerial(port)
serial.open()


for m_ID in range (1, NumMotors+1) :
	pkt = Packet.makeServoSpeedPacket(m_ID, servospeed)  # set servo speed
	serial.sendPkt(pkt)
	sleep(sleep_time)
	pkt = Packet.makeLEDPacket(m_ID, xl320.XL320_LED_OFF)
	serial.sendPkt(pkt)
	sleep(sleep_time)
	pkt = Packet.makeServoPacket(m_ID, start_angle)  # move servo to center
	serial.sendPkt(pkt)  # send packet to servo
	sleep(sleep_time)
# Joystick
try:
	joy = pygame.joystick.Joystick(0)
	joy.init()
	print('joystick is present: ' + joy.get_name())
except pygame.error:
	print ('joystick not found.')

# Main loop

buttons = joy.get_numbuttons()

while True:

	#input ("press a button number from 1 to 6 to select the motor")
	
	#	for i in range(buttons) :
	#		if(joy.get_button(i) == 1):
	#			m_ID = joy.get_button(i)
	#			#print('motor ' +str(m_ID))
	
	joyx,joyy = int(joy.get_axis(0)*maxspeed), int(joy.get_axis(1)*maxspeed)

 	if(joyy<0):
 		gianopirobot.forward(abs(joyy))
 	elif (joyy>0):
 		gianopirobot.backward(abs(joyy))
 	elif (joyy==0):
 		gianopirobot.stop_2_4()

 	if( joyx >0):
 		gianopirobot.goleft(abs(joyx), abs(joyx))
 	elif(joyx<0):
 		gianopirobot.goright(abs(joyx))
 	elif(joyx==0):
 		gianopirobot.stop_1_3()


	if((angle<300)&(angle>=0)):
		pkt = Packet.makeServoPacket(m_ID, angle)
		serial.sendPkt(pkt)
		sleep(sleep_time)
		
		
		
	else:
		angle = start_angle # back to start position
		#print('angle ' + str(angle) + ' out of bound ')

	for event in pygame.event.get():
		if joy.get_button(12) == 1: #PS button
			pygame.quit()
			sys.exit()
			serial.close()
			gianopirobot.stop()

	for i in range(buttons) :

		if(joy.get_button(i) == 1):
			m_ID = i+1
			motorFlag = m_ID 
			pkt = Packet.makeLEDPacket(m_ID, led_color)
			serial.sendPkt(pkt)
			#sleep(sleep_time)
			for id in range(1, NumMotors+1):
				if(id != m_ID):
					pkt = Packet.makeLEDPacket(id, xl320.XL320_LED_OFF)
					serial.sendPkt(pkt)

			#print('motor ' +str(m_ID))

	if event.type == pygame.locals.JOYHATMOTION: # 9
		if((event.value == (0,1))|(event.value == (1,0))) :
			angle = angle + 10
			#print ('motor ' +str(m_ID) + ' event : ' +str(event.type) + ' angle: ' + str(angle) + ' value ' + str(event.value))
			
		elif((event.value == (0,-1))|(event.value == (-1,0))) :
			angle = angle - 10
			#print ('motor ' +str(m_ID) + ' event : ' +str(event.type) + ' angle: ' + str(angle) + ' value ' + str(event.value))


	fpsClock.tick(fps)

atexit.register(gianopirobot.stop())


"""
try:
	led_color = 0
	while True:
		led_color = led_color % 7 + 1
		for m_ID in range (1, NumMotors+1) :
			pkt = Packet.makeLEDPacket(m_ID, led_color)
			serial.sendPkt(pkt)
			for angle in range(0, 300, 10):
				pkt = Packet.makeServoPacket(m_ID, angle)
				serial.sendPkt(pkt)
				sleep(sleep_time)

			led_color = led_color % 7 + 1
			pkt = Packet.makeLEDPacket(m_ID, led_color)
			serial.sendPkt(pkt)
			for angle in range(300, 0, -10):
				pkt = Packet.makeServoPacket(m_ID, angle)
				serial.sendPkt(pkt)
				sleep(sleep_time)
except:
	e = sys.exc_info()[0]
	print(e)
	sleep(0.25)
	for m_ID in range (1, NumMotors+1) :
		pkt = Packet.makeLEDPacket(m_ID, xl320.XL320_LED_OFF)
		serial.sendPkt(pkt)
		pkt = Packet.makeServoPacket(m_ID, 150.0)  # move servo to center
		serial.sendPkt(pkt)  # send packet to servo
		serial.close()
"""
