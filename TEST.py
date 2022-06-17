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
robot = DriveBase(lMotor, rMotor, wheel_diameter=55.5, axle_track=120) #to check next week

ultraSLimit = 100

SILVER = 90
DRIVE_SPEED = 100
TURN_DRIVE_SPEED = 60
WHITE = 50
BLACK = 10
helloMessages = ["Hello there", "Hello mr Dharma", "YOU NILLY SUSAN", "Hello mr Hu", "GET RICKROLLED", "JELLY", "POTATOES", "REFRACTION BEST", "HACK ON 2B2T PLS", "COMMUNISM"]

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
	ev3.speaker.say("Obstacle detected")
	robot.turn(-90)
	robot.curve(ultraS, 180)
	while not isBlack(lColor) and not isBlack(rColor):
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
		multiplier = 1.5
		compensator = 5
		#finds the difference between the reflections
		error = lColor.reflection() - rColor.reflection()
		if leftIsBlack and rightIsBlack:
			turnValue = 0
			ev3.speaker.beep()
			if rColor <= WHITE and rColor >= BLACK:
				robot.turn(50)
			else:
				robot.turn(-50)
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

	
	
	
	
	
