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
motorB = Motor(Port.D)
colorA = ColorSensor.reflection(ColorSensor(Port.S1))
colorB = ColorSensor.reflection(ColorSensor(Port.S4))
ultraS = UltrasonicSensor(Port.S3)
robot = DriveBase(motorA, motorB, wheel_diameter=55.5, axle_track=104) #to check next week

BLACK = reflection(0 - 20)
WHITE = reflection(20 - 90)
SILVER = reflection(90 - 100)
DRIVE_SPEED = 100
# Write your program here.
def findPath():
    driveB.stop()
    time = 0
    while True:
        if time >= 360:
            return False
        driveB.turn(1, True)
        if colorA == BLACK or colorB == BLACK:
            return True
        time += 1
            
        
        
def move():
    while True:
        if colorA == BLACK and colorB == BLACK: 
            driveB.drive(DRIVE_SPEED)
        elif not colorA == BLACK and not colorB == BLACK:
            path = findPath()
            if path:
                pass
            else:
                break
        while colorA == BLACK and colorB == BLACK:
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
        while colourB == WHITE
        robot.straight
    elif colourB == BLACK:
        
        
        