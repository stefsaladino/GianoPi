import GianoPi
import time

M1_TRIM = 0
M2_TRIM = 0
M3_TRIM = 0
M4_TRIM = 0

gianopirobot = GianoPi.GianoPi(m1_trim=-10, m2_trim=M2_TRIM, m3_trim=M3_TRIM, m4_trim=M4_TRIM)


distance = gianopirobot.get_leftobjectdistance()

while (distance >200):
    print distance
    gianopirobot.goright(50)
    distance = gianopirobot.get_leftobjectdistance()

gianopirobot.stop()
