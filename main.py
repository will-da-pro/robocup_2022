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

lMotor = Motor(Port.A)
rMotor = Motor(Port.D)
claw = Motor(Port.C)
lColour = ColorSensor.reflection(ColorSensor(Port.S1))
rColour = ColorSensor.reflection(ColorSensor(Port.S4))
ultraS = UltrasonicSensor(Port.S3)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55.5, axle_track=104) #to check next week

BLACK = 0 - 20
WHITE = 20 - 90
SILVER = 90 - 100
DRIVE_SPEED = 100
# Write your program here.
def findPath():
    robot.stop()
    time = 0
    while True:
        if time >= 360:
            return False
        robot.turn(1, True)
        if lColour == BLACK or rColour == BLACK:
            return True
        time += 1
            
        
        
def move():
    while True:
        if lColour == BLACK and rColour == BLACK:
            robot.drive(DRIVE_SPEED)
        elif not lColour == BLACK and not rColour == BLACK:
            path = findPath()
            if path:
                pass
            else:
                break
        while lColour == BLACK and rColour == BLACK:
            pass


def startup():
    ev3.speaker.say("Initialising Startup")


def obstacle():
    if ultraS.distance() < 100:
        wait(10)
        robot.straight(-100)
        robot.turn(120)
        robot.straight(300)
        robot.turn(45)
        while rColour == WHITE:
            robot.straight(300)
    elif rColour == BLACK:
        robot.stop()

robot.startup()
robot.move()