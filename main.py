#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
import random


# This program requires LEGO EV3 MicroPython v2.0 or higher. (INSTALLED)
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
time_secs = time


lColor = ColorSensor(Port.S1)
rColor = ColorSensor(Port.S4)
lMotor = Motor(Port.A)
rMotor = Motor(Port.D)
claw = Motor(Port.C)
ultraS = UltrasonicSensor(Port.S3)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55.5, axle_track=120) #to check next week

ultraSLimit = 100

SILVER = 90
DRIVE_SPEED = 100
TURN_DRIVE_SPEED = 60
WHITE = 50
BLACK = 20
helloMessages = ["Hello there!", "Hello mr Dharma", "YOU NILLY SUSAN!!!", "Hello mr Hu", "GET RICKROLLED!!!"]

#State variables
fastTurning = False

# Write your program here.
#Runs when one of the colour sensors detects black
def turn(side, degrees):
    startTime = time_secs.time()
    while isBlack(side):
        robot.drive(TURN_DRIVE_SPEED, degrees)
        #TODO Create variable for state
        if time_secs.time() - startTime >= 0.2:

            print("Worked!")
            robot.stop()
            lMotor.run(degrees)
            rMotor.run(degrees - degrees*2)

def findPath():
    robot.stop()
    runTime = 0
    while True:
        if (runTime >= 360):
            return False
        robot.turn(10)
        #If either sensor detects white, it will return to the move function and continue normally
        if (isBlack(lColor) or isBlack(rColor)):
            return True
        runTime += 1 

#Runs if an obstacle is detected
def obstacle():
    wait(5)
    robot.straight(-100)
    robot.turn(120)
    robot.straight(300)
    while lColor.reflection() <= BLACK and rColor.reflection() <= BLACK:
        pass
			
def isBlack(side):
	if side.reflection() <= BLACK:
		return True
	else:
		return False

			
#Handles all movement
def move():
    while True:
        leftIsBlack = isBlack(lColor)
        rightIsBlack = isBlack(rColor)
        if (ultraS.distance() < ultraSLimit):
            pass
        #If both sensors detect white, the robot moves in a straight line
        if (not leftIsBlack and not rightIsBlack):
            robot.drive(DRIVE_SPEED, 0)
        #If the left sensor detects black, then the robot will turn left
        elif (leftIsBlack):
            turn(lColor, -60)
        #If the right sensor detects black, then the robot will turn right
        elif (rightIsBlack):
            turn(rColor, 60)
        #If both sensors detect black, then the find path function will run
        else:
            path = findPath()
            if path:
                pass
            else:
                break

def startMessage():
    #Arguments should be 1 and the number of possible outcomes
    rand = random.randint(0, len(helloMessages) - 1)
    ev3.speaker.say(helloMessages[rand])
    
startMessage()

move()

    
    
    
    
    
