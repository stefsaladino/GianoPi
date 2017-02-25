
from SimpleCV import *


cam = Camera()
threshold = 5.0
while True:
    previous = cam.getImage()
    time.sleep(0.5)
    current = cam.getImage()
    diff = current -previous
    matrix = diff.getNumpy()
    mean = matrix.mean()
    diff.show()
    if mean >= threshold:
        print "Motion detected"
