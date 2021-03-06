from Adafruit_MotorHAT import Adafruit_MotorHAT,Adafruit_DCMotor
import time

mh = Adafruit_MotorHAT(addr=0x60)
motor1 = mh.getMotor(1)
motor2 = mh.getMotor(2)
motor3 = mh.getMotor(3)
motor4 = mh.getMotor(4)


def turnClockwise(angle):
    motor1.run(Adafruit_MotorHAT.FORWARD)
    motor2.run(Adafruit_MotorHAT.FORWARD)
    motor3.run(Adafruit_MotorHAT.FORWARD)
    motor4.run(Adafruit_MotorHAT.FORWARD)

    motor1.setSpeed(150)
    motor2.setSpeed(150)
    motor3.setSpeed(150)
    motor4.setSpeed(150)

    time.sleep((angle/90)*0.75) #0.75s is a 90 degrees
    
    motor1.run(Adafruit_MotorHAT.RELEASE)
    motor2.run(Adafruit_MotorHAT.RELEASE)
    motor3.run(Adafruit_MotorHAT.RELEASE)
    motor4.run(Adafruit_MotorHAT.RELEASE)

def turnAntiClockwise(angle):
    motor1.run(Adafruit_MotorHAT.FORWARD)
    motor2.run(Adafruit_MotorHAT.FORWARD)
    motor3.run(Adafruit_MotorHAT.FORWARD)
    motor4.run(Adafruit_MotorHAT.FORWARD)

    motor1.setSpeed(150)
    motor2.setSpeed(150)
    motor3.setSpeed(150)
    motor4.setSpeed(150)

    time.sleep((angle/90)*0.75) #0.75s is a 90 degrees
    
    motor1.run(Adafruit_MotorHAT.RELEASE)
    motor2.run(Adafruit_MotorHAT.RELEASE)
    motor3.run(Adafruit_MotorHAT.RELEASE)
    motor4.run(Adafruit_MotorHAT.RELEASE)

def turn(angle):
    if (angle >0):
        turnClockwise(angle)
    else:
        turnAntiClockwise(angle)
"""
def turnClockwise():
    motor1.run(Adafruit_MotorHAT.FORWARD)
    motor1.setSpeed(150)
    motor3.run(Adafruit_MotorHAT.FORWARD)
    motor3.setSpeed(150)
    time.sleep(0.5)
    motor1.run(Adafruit_MotorHAT.RELEASE)
    motor3.run(Adafruit_MotorHAT.RELEASE)
"""
while (True):
    angle = float(input("enter an angle: "))
    turn(angle)

#turnAnticlockwise()
