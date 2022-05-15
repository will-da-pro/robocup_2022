#Made for robocup 2022
#By William, Bain and Toby at SGCS
#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
import random
import logging


# This program requires LEGO EV3 MicroPython v2.0 or higher. (INSTALLED)
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
time_secs = time

#Initialize all robot variables
lColour = ColorSensor(Port.S1)
rColour = ColorSensor(Port.S4)
lMotor = Motor(Port.A)
rMotor = Motor(Port.D)
claw = Motor(Port.C)
ultraS = UltrasonicSensor(Port.S3)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55.5, axle_track=120) #to check next week

#Other variables
ultraSLimit = 100
SILVER = 90
DRIVE_SPEED = 100
TURN_DRIVE_SPEED = 60
WHITE = 50
BLACK = 20

# Write your program here.

#Runs when one of the colour sensors detects black
def turn(side, degrees):
    #Starts a timer
    startTime = time_secs.time()
    while side.reflection() <= BLACK:
        robot.drive(TURN_DRIVE_SPEED, degrees)
        #Afer 0.2 seconds, it starts turning faster.
        if time_secs.time() - startTime >= 0.2:
            robot.drive(TURN_DRIVE_SPEED, degrees * 2.3) 

#Rotates until a path is detected.             
def findPath():
    robot.stop()
    #Each time the robot turns, it will increase this variable
    runTime = 0
    while True:
        #If the robot has failed to locate a path after turning 360 degrees, it will return false stopping the program
        if (runTime >= 36):
            return False
        robot.turn(10)
        #If either sensor detects white, it will return to the move function and continue normally
        if (lColour.reflection() >= BLACK or rColour.reflection() >= BLACK):
            return True
        runTime += 1 

#Runs if an obstacle is detected
def obstacle():
    wait(5)
    robot.straight(-100)
    robot.turn(120)
    robot.straight(300)
    while lColour.reflection() <= BLACK and rColour.reflection() <= BLACK:
        pass

#Handles all movement
def move():
    while True:
        if (ultraS.distance() < ultraSLimit):
            #obstacle()
            pass
        #If both sensors detect white, the robot moves in a straight line
        if lColour.reflection() >= BLACK and rColour.reflection() >= BLACK:
            robot.drive(DRIVE_SPEED, 0)
        #If the left sensor detects black, then the robot will turn left
        elif lColour.reflection() <= BLACK:
            turn(lColour, -60)
        #If the right sensor detects black, then the robot will turn right
        elif rColour.reflection() <= BLACK:
            turn(rColour, 60)
        #If both sensors detect black, then the find path function will run
        else:
            path = findPath()
            if path:
                #If a path is found, the function will continue normally
                pass
            else:
                #If no path is found then the function will break
                break

def startMessage():
    #Arguments should be 1 and the number of possible outcomes
    rand = random.randint(1, 3)
    match rand:
        case 1:
            ev3.speaker.say("HELLLO MR DHARMA")
        case 2: 
            ev3.speaker.say("YOU NILLY SUSAN")
        case 3:
            ev3.speaker.say("HELLO THERE")
        case _:
            logging.error("Invalid start message. Did you update the random variable?")
        
startMessage()
#Start movement
move()

    
    
    
    
    
