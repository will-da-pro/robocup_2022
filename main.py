#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time


# This program requires LEGO EV3 MicroPython v2.0 or higher. (INSTALLED)
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


lColour = ColorSensor(Port.S1)
rColour = ColorSensor(Port.S4)
lMotor = Motor(Port.A)
rMotor = Motor(Port.D)
claw = Motor(Port.C)
ultraS = UltrasonicSensor(Port.S3)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55.5, axle_track=120) #to check next week

ultraSLimit = 100

SILVER = 90
DRIVE_SPEED = 100
TURN_DRIVE_SPEED = 50
WHITE = 50
BLACK = 20

# Write your program here.




def findPath():
    robot.stop()
    runTime = 0
    while True:
        if (runTime >= 360):
            return False
        robot.turn(10)
        if (lColour.reflection() <= BLACK or rColour.reflection() <= BLACK):
            return True
        runTime += 1    

def move():
    while True:

        if (ultraS.distance() < ultraSLimit):
            #obstacle()
            pass
        if lColour.reflection() >= BLACK and rColour.reflection() >= BLACK:
            robot.drive(DRIVE_SPEED, 0)
        elif lColour.reflection() <= BLACK:
            robot.drive(TURN_DRIVE_SPEED, -100)
            while lColour.reflection() <= BLACK:
                pass
        elif rColour.reflection() <= BLACK:
            robot.drive(TURN_DRIVE_SPEED, 100)
            while rColour.reflection() <= BLACK:
                pass
        else:
            path = findPath()
            if path:
                pass
            else:
                break

def obstacle():
    wait(10)
    robot.straight(-100)
    robot.turn(120)
    robot.straight(300)
    while lColour.reflection() <= BLACK and rColour.reflection() <= BLACK:
        pass

        
ev3.speaker.say("MR DHARMA")

move()

    
    
    
    
    
