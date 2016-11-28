# Simply read adc values . by Stefania Saladino)
#

import time

# Import the GianoPi.py file (must be in the same directory as this file!).
import GianoPi



# Create an instance of the robot 


gianopirobot = GianoPi.GianoPi()

# Now test 4 ground sensors

while(True):
    four_line_sensors = gianopirobot.get_ground_sensors()
    for i in range (4):
    print "C[",i,"] = ", four_line_sensors[i]
 
