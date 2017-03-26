import time
sys.path.insert(1, os.path.join(sys.path[0], '../..'))
import GianoPi


import atexit
import RPi.GPIO as GPIO

from Adafruit_MotorHAT import Adafruit_MotorHAT

gianopirobot = GianoPi.GianoPi()
gianopirobot.stop()
time.sleep(2.0)   

GPIO.cleanup()
atexit.register(gianopirobot.stop())      # Stop the robot
