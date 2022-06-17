#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor, Motor)
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
robot = DriveBase(lMotor, rMotor, wheel_diameter=55.5, axle_track=120) #incorrect, but will stay with it...

ultraSLimit = 100

SILVER = 90
DRIVE_SPEED = 100
TURN_DRIVE_SPEED = 60
WHITE = 50
BLACK = 20
helloMessages = ["Hello there", "Hello mr Dharma", "YOU NILLY SUSAN", "Hello mr Hu", "GET RICKROLLED", "JELLY", "POTATOES", "REFRACTION BEST", "HACK ON 2B2T PLS", "COMMUNISM", "What do you think you are doing", "More start messages means more lag", "yes", "parp", "kathmandu", "what you doing", "hypixel skyblock hype is op", "water tower", "you mrs leech", "you mrs walnut", "hello smoothiedrew", "gas", "andrew's toxic gas", "whale", "scatha", "will is good", "worms", "thats long", "ratfraction is cal but on vape", "rise client is meta", "now for water tower", "wheres the water tower", "laughing", "why are you making so many", "failure", "stop now its too long", "this is smooth"]

#State variables
fastTurning = False

# Write your program here.
#Runs when one of the colour sensors detects black
def turn(side, degrees):
	fastTurning = False
	startTime = time_secs.time()
	while isBlack(side):
		robot.drive(TURN_DRIVE_SPEED, degrees)
		if (time_secs.time() - startTime >= 0.15):
			if not fastTurning:
				robot.stop()
				fastTurning = True
				ev3.speaker.beep()
				rMotor.run(-degrees * 2)
				lMotor.run(degrees * 2)
	fastTurning = False

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
	robot.stop()
	ev3.speaker.say("Obstacle detected")
	distance = ultraS.distance()
	robot.turn(-90)
	robot.curve(distance, 180, Stop.HOLD, wait=False)
	while not isBlack(lColor) and not isBlack(rColor):
		pass
	robot.turn(-90)
			
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
			obstacle()
		#If both sensors detect white, the robot moves in a straight line
		#if (not leftIsBlack and not rightIsBlack):
			#robot.drive(DRIVE_SPEED, 0)
		#If the left sensor detects black, then the robot will turn left
		#elif (leftIsBlack):
			#turn(lColor, -140)
		#If the right sensor detects black, then the robot will turn right
		#elif (rightIsBlack):
			#turn(rColor, 140)
		#If both sensors detect black, then the find path function will run
		#Amount to multiply output by
		multiplier = 2.1
		compensator = 5
		#finds the difference between the reflections
		error = lColor.reflection() - rColor.reflection()
		if leftIsBlack and rightIsBlack:
			turnValue = 0
			ev3.speaker.beep()
			#if error <= compensator and error >= -compensator:
			#	robot.drive(TURN_DRIVE_SPEED, turnValue * 2)
			if lColor.reflection() <= rColor.reflection():
				robot.turn(30)
				robot.straight(40)
			else:
				robot.turn(-30)
				robot.straight(40)
		#gets degrees to turn by
		output = int(multiplier * (error))
		#output may need to be limited to within -180, 180
		robot.drive(DRIVE_SPEED, output)
		c = 1
		if c == 0:
			ev3.speaker.beep()
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

	
	
	
	
	
