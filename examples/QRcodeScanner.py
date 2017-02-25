import zbar
from SimpleCV import *


cam = Camera()
display = Display()
while(display.isNotDone()):
    img = cam.getImage()
    barcode = img.findBarcode()
    if(barcode is not None):
        barcode = barcode[0]
        result = str(barcode.data)
        print result
        barcode = []
        img.save(display)
