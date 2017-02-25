#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import RPi.GPIO as GPIO
#import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        # if ((adcnum > 7) or (adcnum < 0)):
        if (adcnum > 7):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 19 # was 18
SPIMISO = 20 # was 23
SPIMOSI = 12 # was 24
SPICS = 25 #was 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# photodiode sensor connected to adc #0
ch1_adc = 0;
ch2_adc = 1;
ch3_adc = 2;
ch4_adc = 3;
ch5_adc = 4;
ch6_adc = 5;
ch7_adc = 6;
ch8_adc = 7;

while True:

        # read the analog pin
        adc_1 = readadc(ch1_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        adc_2 = readadc(ch2_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        adc_3 = readadc(ch3_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        adc_4 = readadc(ch4_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # adc_5 = readadc(ch5_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # adc_6 = readadc(ch6_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # adc_7 = readadc(ch7_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        # adc_8 = readadc(ch8_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

        
        print "1,2,3,4 ", adc_1, adc_2, adc_3, adc_4
        print " " 
        

        # hang out and do nothing for a half second
        time.sleep(0.5)
