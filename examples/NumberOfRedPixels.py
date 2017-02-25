from picamera.array import PiRGBArray
from picamera import PiCamera
from SimpleCV import Image, Color
import time

w = 320
h = 240
threshold = 64

camera = PiCamera()
camera.resolution = (w,h)

rawcapture = PiRGBArray(camera)
camera.capture(rawcapture, format= 'rgb')

img = Image(rawcapture.array)

red_object = img.colorDistance(Color.RED)
red_object.show()
time.sleep(1)

matrix = red_object.getNumpy()

#print matrix
c = 0
for i in range (0, h-1):
    for l in range (0, w-1):
        if matrix[i,l,0] <= threshold :
            c+=1
           # print matrix[i,l,0], i, l

percentage = 100.00*c/(w*h)

print "Percentage of Red pixels at threshold = ", threshold, " is ", percentage, "% Number =", c  
