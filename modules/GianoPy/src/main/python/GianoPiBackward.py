# Simple two DC motor robot class usage example.
# Author: Tony DiCola (adapted by Stefania Saladino)
# License: MIT License https://opensource.org/licenses/MIT
import time

# Import the GianoPi.py file (must be in the same directory as this file!).
import GianoPi


# Set the trim offset for each motor (1,2,3,4).  This is a value that
# will offset the speed of movement of each motor in order to make them both
# move at the same desired speed.  Because there's no feedback the robot doesn't
# know how fast each motor is spinning and the robot can pull to a side if one
# motor spins faster than the other motor.  To determine the trim values move the
# robot forward slowly (around 100 speed) and watch if it veers to the left or
# right.  If it veers left then the _right_ motor is spinning faster so try
# setting RIGHT_TRIM to a small negative value, like -5, to slow down the right
# motor.  Likewise if it veers right then adjust the _left_ motor trim to a small
# negative value.  Increase or decrease the trim value until the bot moves
# straight forward/backward.
M1_TRIM   = 0
M2_TRIM  = 0
M3_TRIM = 0
M4_TRIM = 0

# Create an instance of the robot with the specified trim values.
# Not shown are other optional parameters:
#  - addr: The I2C address of the motor HAT, default is 0x60.
#  - mn_id: The ID of the left motor, default is 1 for the motor opposite to GPIO,
# nearest to HAT cable.

gianopirobot = GianoPi.GianoPi(m1_trim=M1_TRIM, m2_trim=M2_TRIM, m3_trim=M3_TRIM, m4_trim=M4_TRIM)

# Now move the robot around!
# Each call below takes two parameters:
#  - speed: The speed of the movement, a value from 0-255.  The higher the value
#           the faster the movement.  You need to start with a value around 100
#           to get enough torque to move the robot.
#  - time (seconds):  Amount of time to perform the movement.  After moving for
#                     this amount of seconds the robot will stop.  This parameter
#                     is optional and if not specified the robot will start moving
#                     forever.

gianopirobot.forward(150, 1.0)   # Move forward at speed 150 for 1 second.
gianopirobot.goleft(200, 0.5)      # Spin left at speed 200 for 0.5 seconds.
gianopirobot.forward(150, 1.0)   # Repeat the same movement 3 times below...
gianopirobot.goleft(200, 0.5)
gianopirobot.forward(150, 1.0)
gianopirobot.goleft(200, 0.5)
gianopirobot.forward(150, 1.0)
gianopirobot.goright(200, 0.5)

# Spin in place slowly for a few seconds.
gianopirobot.goright(100)  # No time is specified so the robot will start spinning forever.
time.sleep(2.0)   # Pause for a few seconds while the robot spins (you could do
                  # other processing here though!).
gianopirobot.stop()      # Stop the robot from moving.

# Now move backwards and spin right a few times.
gianopirobot.backward(150, 1.0)
gianopirobot.goright(200, 0.5)
gianopirobot.backward(150, 1.0)
gianopirobot.goright(200, 0.5)
gianopirobot.backward(150, 1.0)
gianopirobot.goright(200, 0.5)
gianopirobot.backward(150, 1.0)

# That's it!  Note that on exit the robot will automatically stop moving.


