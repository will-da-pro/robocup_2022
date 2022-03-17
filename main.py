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

motorA = Motor(Port.B)
motorB = Motor(Port.D)
colorA = ColorSensor(Port.1)
colorB = ColorSensor(Port.4)
ultraS = UltrasonicSensor(Port.3)
# Write your program here.
def move():
    while True:
def startup():
    ev3.speaker.say("Initialising Startup")
    
    