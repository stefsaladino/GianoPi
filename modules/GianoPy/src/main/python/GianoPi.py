# Four DC motor holonomic robot class named GianoPi.  Exposes a simple LOGO turtle-like API for
# moving a robot forward, backward, Portside, starboard and turning.  
# Motor 1 sits opposite to GPIO, GPIO is the "Front", 2, 3, 4 are the motors when counting clockwise 
# and looking from the top of the robot
# See GianoPiTest.py for an
# example of using this class.
# Author: Stefania Saladino - as from Adafruit Robot.py example

import time
import atexit

from Adafruit_MotorHAT import Adafruit_MotorHAT


class GianoPi(object):
    def __init__(self, addr=0x60, m1_id=1, m2_id=2, m3_id=3, m4_id=4,
                 m1_trim=0, m2_trim=0, m3_trim=0, m4_trim=0,
                 stop_at_exit=True):
        """Create an instance of the robot.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x60.
         - m1_id: The ID of the first motor (physically opposite to GPIO) , default is 1.
         - m1_trim: Amount to offset the speed of the left motor, can be positive
                      or negative and use useful for matching the speed of both
                      motors.  Default is 0.
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        """
        # Initialize motor HAT motors.
        self._mh = Adafruit_MotorHAT(addr)
        self._m1 = self._mh.getMotor(m1_id)
        self._m2 = self._mh.getMotor(m2_id)
        self._m3 = self._mh.getMotor(m3_id)
        self._m4 = self._mh.getMotor(m4_id)
        self._m1_trim=m1_trim
        self._m2_trim=m2_trim
        self._m3_trim=m3_trim
        self._m4_trim=m4_trim
        
        # Start with motors turned off.
        self._m1.run(Adafruit_MotorHAT.RELEASE)
        self._m2.run(Adafruit_MotorHAT.RELEASE)
        self._m3.run(Adafruit_MotorHAT.RELEASE)
        self._m4.run(Adafruit_MotorHAT.RELEASE)
        
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)

    def _m1_speed(self, speed):
        """Set the speed of the m1 motor.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._m1_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._m1.setSpeed(speed)
        
    def _m2_speed(self, speed):
        """Set the speed of the m2 motor.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._m2_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._m2.setSpeed(speed)
        
    def _m3_speed(self, speed):
        """Set the speed of the m3 motor.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._m3_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._m3.setSpeed(speed)
        
    def _m4_speed(self, speed):
        """Set the speed of the m4 motor.
        """
        assert 0 <= speed <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        speed += self._m4_trim
        speed = max(0, min(255, speed))  # Constrain speed to 0-255 after trimming.
        self._m4.setSpeed(speed)


    def stop(self):
        """Stop all movement."""
        self._m1.run(Adafruit_MotorHAT.RELEASE)
        self._m2.run(Adafruit_MotorHAT.RELEASE)
        self._m3.run(Adafruit_MotorHAT.RELEASE)
        self._m4.run(Adafruit_MotorHAT.RELEASE)

    def forward(self, speed, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the robot will move forward for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._m2_speed(speed)
        self._m4_speed(speed)
        self._m2.run(Adafruit_MotorHAT.BACKWARD)
        self._m4.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, speed, seconds=None):
        """Move backward at the specified speed (0-255).  Will start moving
        backward and return unless a seconds value is specified, in which
        case the robot will move backward for that amount of time and then stop.
        """
        # Set motor speed and move both backward.
        self._m2_speed(speed)
        self._m4_speed(speed)
        self._m2.run(Adafruit_MotorHAT.BACKWARD)
        self._m4.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()
            
    def goleft(self, speed, seconds=None):
        """Move to the left at the specified speed (0-255).  Will start moving
        left and return unless a seconds value is specified, in which
        case the robot will move left for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._m1_speed(speed)
        self._m3_speed(speed)
        self._m1.run(Adafruit_MotorHAT.FORWARD)
        self._m3.run(Adafruit_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def goright(self, speed, seconds=None):
        """Move to the right at the specified speed (0-255).  Will start moving
        right and return unless a seconds value is specified, in which
        case the robot will move right for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._m1_speed(speed)
        self._m3_speed(speed)
        self._m1.run(Adafruit_MotorHAT.BACKWARD)
        self._m3.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()
            
            
    def turnright_m1_m3(self, speed, seconds=None):
        """Spin to the right at the specified speed using m1 and m3.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._m1_speed(speed)
        self._m3_speed(speed)
        self._m1.run(Adafruit_MotorHAT.BACKWARD)
        self._m3.run(Adafruit_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def turnleft_m1_m3(self, speed, seconds=None):
        """Spin to the left at the specified speed using m1 and m3.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._m1_speed(speed)
        self._m3_speed(speed)
        self._m1.run(Adafruit_MotorHAT.FORWARD)
        self._m3.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()
            
    def turnright_m2_m4(self, speed, seconds=None):
        """Spin to the right at the specified speed using m2 and m4.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._m2_speed(speed)
        self._m4_speed(speed)
        self._m2.run(Adafruit_MotorHAT.BACKWARD)
        self._m4.run(Adafruit_MotorHAT.BACKWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def turnleft_m2_m4(self, speed, seconds=None):
        """Spin to the left at the specified speed using m2 and m4.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._m2_speed(speed)
        self._m4_speed(speed)
        self._m2.run(Adafruit_MotorHAT.FORWARD)
        self._m4.run(Adafruit_MotorHAT.FORWARD)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()