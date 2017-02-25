import GianoPi
import time
import atexit
import RPi.GPIO as GPIO

M1_TRIM = 0
M2_TRIM = 0
M3_TRIM = 0
M4_TRIM = 0

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
Luno = 0
L2 = 0
L3 = 0
L4 = 0

print "Put the robot on a Black surface"
time.sleep(4)
for i in range(0, 10):
    line_sensors = gianopirobot.get_ground_sensors(list)
    Luno = Luno + line_sensors[0] 
    L2 = L2 + line_sensors[1] 
    L3 = L3 + line_sensors[2]
    L4 = L4 + line_sensors[3]
##    print Luno, line_sensors[0],L2,line_sensors[1], L3,line_sensors[2],L4,line_sensors[3]
                             
Luno = Luno/10.00
L2 = L2/10.000
L3 = L3/10.000
L4 = L4/10.00    

print "On Black ", Luno, L2, L3, L4   
Luno = 0
L2 = 0
L3 = 0
L4 = 0
                               
print "Put the robot on a White surface"
time.sleep(4)                           
for i in range(0, 10):
    line_sensors = gianopirobot.get_ground_sensors(list)
    Luno = Luno + line_sensors[0] 
    L2 = L2 + line_sensors[1] 
    L3 = L3 + line_sensors[2]
    L4 = L4 + line_sensors[3]
                               
Luno = Luno/10.00
L2 = L2/10.00
L3 = L3/10.00
L4 = L4/10.00    

print "On White ", Luno, L2, L3, L4   
    
GPIO.cleanup()

