#MRS OLLERTON LOVES 8
#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher. (INSTALLED)
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

motorA = Motor(Port.A)
motorB = Motor(Port.B)
colorA = ColorSensor.reflection(ColorSensor(Port.S1))
colorB = ColorSensor.reflection(ColorSensor(Port.S4))
ultraS = UltrasonicSensor(Port.S3)
driveB = DriveBase(motorA, motorB, wheel_diameter=55.5, axle_track=104)

BLACK = 0 - 20
WHITE = 20 - 90
DRIVE_SPEED = 100

deviation = line_sensor.reflection() - threshold
turn_rate = PROPORTIONAL_GAIN * deviation
robot.drive(DRIVE_SPEED, turn_rate)

color = ColorSensor.reflection() 
# Write your program here.
def findPath():
    while True:
        driveB.turn(1, True)
        if 
        
        
def move():
    while True:
        if colorA and colorB == reflection: 
            driveB.drive(1)
        elif not colorA and not colorB == reflection:
            findPath()
        while colorA and colorB == reflection:
            pass
def startup():
    ev3.speaker.say("Initialising Startup")
    
