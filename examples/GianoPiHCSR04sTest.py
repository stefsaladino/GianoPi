# Simple two DC motor robot class usage example.
# Author: Tony DiCola (adapted by Stefania Saladino)
# License: MIT License https://opensource.org/licenses/MIT
import time

# Import the GianoPi.py file (must be in the same directory as this file!).
import GianoPi



# Create an instance of the robot with the specified trim values.
# Not shown are other optional parameters:
#  - addr: The I2C address of the motor HAT, default is 0x60.
#  - mn_id: The ID of the motor.

gianopirobot = GianoPi.GianoPi()

# Now test ultrasonic sensors

while(True):
    rightdis = gianopirobot.get_rightobjectdistance()
    print "Object detected at RIGHT! Distance:",rightdis,"cm"
    frontdis = gianopirobot.get_fronttobjectdistance()
    print "Objetb detected in front! Distance:",frontdis,"cm"
