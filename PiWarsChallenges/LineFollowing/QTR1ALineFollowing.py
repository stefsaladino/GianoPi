import GianoPi
import time
import atexit
import RPi.GPIO as GPIO

M1_TRIM = 0
M2_TRIM = 0
M3_TRIM = 0
M4_TRIM = -70 #today 15/01/2017

GPIO.setmode(GPIO.BCM)

# the following are  the pins connected from the Pi on the ADC
SPICLK = 19 
SPIMISO = 20 
SPIMOSI = 12 
SPICS = 25 

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

gianopirobot = GianoPi.GianoPi(m1_trim=-10, m2_trim=M2_TRIM, m3_trim=M3_TRIM, m4_trim=M4_TRIM)

list = [1,1,1,1]

#gianopirobot.forward(50)
TURNSPEED = 100
SIDESPEED = 80
SPEED = 130
BLACK = 600

while(True):
    line_sensors = gianopirobot.get_ground_sensors(list)
    #for i in range(0, 4): print i, " ,", line_sensors
    if (line_sensors[0] > BLACK)&(line_sensors[3] > BLACK):
        gianopirobot.forward(SPEED, seconds = 0.1)
        #print "FORWARD, ", line_sensors[1],line_sensors[2]
    while (line_sensors[0] <= BLACK)&(line_sensors[3] > BLACK):
        gianopirobot.turnleft_m2_m4(TURNSPEED, seconds=0.1)
        gianopirobot.goright(SIDESPEED, seconds = 0.1)
        line_sensors = gianopirobot.get_ground_sensors(list)
        #print "TURN LEFT, ", line_sensors[1],line_sensors[2]
    while (line_sensors[0] > BLACK)&(line_sensors[3] <= BLACK):
        gianopirobot.turnright_m2_m4(TURNSPEED, seconds=0.1)
        gianopirobot.goleft(SIDESPEED, seconds = 0.1)
        line_sensors = gianopirobot.get_ground_sensors(list)
        #print "TURN RIGHT, ",line_sensors[1],line_sensors[2]
    if (line_sensors[0] <= BLACK  & line_sensors[3] <= BLACK):
        gianopirobot.stop()
        #print "STOP, ", line_sensors[1],line_sensors[2]

        
atexit.register(gianopirobot.stop())
GPIO.cleanup()

