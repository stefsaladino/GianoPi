#!/usr/bin/env python
from __future__ import division, print_function
import pygame, datetime, sys, os
from pygame.locals import *
import atexit
from time import sleep
from pyxl320 import ServoSerial
from pyxl320 import Packet, xl320
import colorsys
import numpy as np
from blinkt import set_clear_on_exit, set_pixel, show, set_brightness
import time


sys.path.insert(1, os.path.join(sys.path[0], '../..'))
import GianoPi
gianopirobot = GianoPi.GianoPi()


set_clear_on_exit()

def The_End():
    exec("../../../Pimoroni/blinkt/examples/rainbow.py")


# pygame

pygame.init()
pygame.joystick.init()
fpsClock = pygame.time.Clock()

fps = 10

# Arm
m_ID = 1
port = '/dev/ttyUSB0'
sleep_time = 0.1
servospeed = 0.5
start_angle = 150.0
angle = [150.,150.,150.,150.,150.,150.,150., 150., 150.]
maxspeed = 100 #maxspeed of dc motors
led_color = 2
NumMotors = 6
motorFlag = 0

serial = ServoSerial(port)
serial.open()


for m_ID in range (1, NumMotors+1) :
	set_pixel(m_ID, 255, 0, 0)
	pkt = Packet.makeServoSpeedPacket(m_ID, servospeed)  # set servo speed
	serial.sendPkt(pkt)
	sleep(sleep_time)
	pkt = Packet.makeLEDPacket(m_ID, xl320.XL320_LED_OFF)
	serial.sendPkt(pkt)
	sleep(sleep_time)
	pkt = Packet.makeServoPacket(m_ID, start_angle)  # move servo to center
	serial.sendPkt(pkt)  # send packet to servo
	sleep(sleep_time)
show()
# Joystick
try:
	joy = pygame.joystick.Joystick(0)
	joy.init()
	print('joystick is present: ' + joy.get_name())
except pygame.error:
	print ('joystick not found.')

# Main loop

buttons = joy.get_numbuttons()
m_ID = 1

while True:

	#blinkt a red 
	
	

	# to move the robot
	joyx,joyy = int(joy.get_axis(0)*maxspeed), int(joy.get_axis(1)*maxspeed)

 	if(joyy<0):
 		gianopirobot.forward(abs(joyy), abs(joyy)+5)
 	elif (joyy>0):
 		gianopirobot.backward(joyy)
 	elif (joyy==0):
 		gianopirobot.stop_2_4()

 	if( joyx >0):
 		gianopirobot.goleft(abs(joyx), abs(joyx))
 	elif(joyx<0):
 		gianopirobot.goright(abs(joyx), abs(joyx))
 	elif(joyx==0):
 		gianopirobot.stop_1_3()
	
 	# specific angle for each motor
	if((angle[m_ID]<300)&(angle[m_ID]>=0)):
		pkt = Packet.makeServoPacket(m_ID, angle[m_ID])
		serial.sendPkt(pkt)
		sleep(sleep_time)
			
		
	else:
		angle[m_ID] = start_angle # back to start position
		#print('angle ' + str(angle) + ' out of bound ')

	

	for i in range(buttons) :

		if(joy.get_button(i) == 1):
				m_ID = i+1
				motorFlag = m_ID 
				pkt = Packet.makeLEDPacket(m_ID, led_color)
				serial.sendPkt(pkt)
				lednum = 7-m_ID
				set_pixel(lednum, 0, 255, 0)
				show()
				#sleep(sleep_time)
				for id in range(1, NumMotors+1):
					if(id != m_ID):
						pkt = Packet.makeLEDPacket(id, xl320.XL320_LED_OFF)
						serial.sendPkt(pkt)
						lednum = 7-m_ID
						set_pixel(lednum, 255, 0, 0)
				
			#print('motor ' +str(m_ID))
	
	
	for event in pygame.event.get():

		if joy.get_button(12) == 1: #PS button
			
			gianopirobot.stop()
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
			pygame.quit()
			sys.exit()
			serial.close()

		if event.type == pygame.locals.JOYHATMOTION: # 9
			if((event.value == (0,1))|(event.value == (1,0))) :
				angle[m_ID] = angle[m_ID] + 10
			#print ('motor ' +str(m_ID) + ' event : ' +str(event.type) + ' angle: ' + str(angle) + ' value ' + str(event.value))
			
			elif((event.value == (0,-1))|(event.value == (-1,0))) :
				angle[m_ID] = angle[m_ID] - 10
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
