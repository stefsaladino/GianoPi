#!/usr/bin/env python

import math
import time

from blinkt import set_clear_on_exit, set_pixel, show, set_brightness


set_clear_on_exit()

reds = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0]

start_time = time.time()


    delta = (time.time() - start_time) * 16

    # Sine wave, spends a little longer at min/max
    # offset = int(round(((math.sin(delta) + 1) / 2) * 7))

    # Triangle wave, a snappy ping-pong effect
    offset = int(abs((delta % 16) - 8))

    for i in range(8):
        set_pixel(i , reds[offset + i], 0, 0)
    show()

    time.sleep(10)
