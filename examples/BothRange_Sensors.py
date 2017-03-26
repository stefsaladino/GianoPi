import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG1 = 5 #right object distance
ECHO1 = 13
TRIG2 = 17 #front object distance
ECHO2 = 18

print "Distance from the right - Measurement In Progress"

GPIO.setup(TRIG1,GPIO.OUT)
GPIO.setup(ECHO1,GPIO.IN)

GPIO.output(TRIG1, False)
time.sleep(0.02)
print "Waiting For Sensors To Settle"


GPIO.output(TRIG1, True)
time.sleep(0.00001)
GPIO.output(TRIG1, False)

while GPIO.input(ECHO1)==0:
  pulse_start = time.time()

while GPIO.input(ECHO1)==1:
  pulse_end = time.time()
  
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)

#GPIO.cleanup()
##GPIO.setmode(GPIO.BCM)
#TRIG2 = 17
#ECHO2 = 18
print "Distance from the front - Measurement In Progress"

GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)
GPIO.output(TRIG2, False)
time.sleep(0.02)
print "Distance from the front - Measurement In Progress"

GPIO.output(TRIG2, True)
time.sleep(0.00001)
GPIO.output(TRIG2, False)

while GPIO.input(ECHO2)==0:
  pulse_START = time.time()

while GPIO.input(ECHO2)==1:
  pulse_END = time.time()


pulse2 = pulse_END - pulse_START
distance2 = pulse2 * 17150
distance2 = round(distance2, 2)

print "Distance front:",distance2,"cm"," Distance right:", distance, "cm" 


GPIO.cleanup()

