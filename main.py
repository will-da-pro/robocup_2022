#!/usr/bin/env pybricks-micropython
from curses.ascii import isblank
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor, Motor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time as timeSecs
import random
from math import sqrt, asin


# This program requires LEGO EV3 MicroPython v2.0 or higher. (INSTALLED)
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

#sensors
rColor = ColorSensor(Port.S1)
lColor = ColorSensor(Port.S4)
ultraS = UltrasonicSensor(Port.S3)
ultraSLimit = 90

#motors
rMotor = Motor(Port.A)
lMotor = Motor(Port.D)
claw = Motor(Port.B)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55, axle_track=136) #fixed
clawTurn = 220

#drive speed variables
driveSpeed = 100
turnDriveSpeed = 60

#colors
silver = 90
white = 50
black = 25

#other variables
helloMessages = ["Hello there", "Hello mr Dharma", "YOU NILLY SUSAN", "Hello mr Hu", "GET RICKROLLED", "JELLY", "POTATOES", "REFRACTION BEST", "HACK ON 2B2T PLS", "COMMUNISM", "What do you think you are doing", "More start messages means more lag", "yes", "parp", "kathmandu", "what you doing", "hypixel skyblock hype is op", "water tower", "you mrs leech", "you mrs walnut", "hello smoothiedrew", "gas", "andrew's toxic gas", "whale", "scatha", "will is good", "worms", "thats long", "ratfraction is cal but on vape", "rise client is meta", "now for water tower", "wheres the water tower", "laughing", "why are you making so many", "failure", "stop now its too long", "this is smooth", "more start messages means more life", "Jellybean is mid", "FORTNITE BATTLE PASS", "get the ems", "prot 4 bois", "dont waste your money on a subzero wisp PLEASE", "6b9t is best", "nah I don't know what to say", "UR MUM", "cum in ur mum", "it's getting pretty long", "Mike Oxlong", "Kimmy Head", "Master baiter"]

# Write your program here.

#Runs if an obstacle is detected
def obstacle(distance, speed):
	robot.stop()
	print("[" + str(timeSecs.time()) + "]: Obstacle detected")
	robot.straight(-50)
	robot.turn(-90)
	robot.drive(driveSpeed, 35)	#robot.curve(distance, 180, Stop.HOLD, wait=False)
	wait(30)
	while not isBlack(lColor) and not isBlack(rColor):
		pass
	robot.turn(-60)
	print("[" + str(timeSecs.time()) + "]: Obstacle passed")
			
def isBlack(side):
	if side.reflection() <= black:
		return True
	else:
		return False

def rescue():
	robot.stop()
	print("[" + str(timeSecs.time()) + "]: Rescue initiated")
	print(robot.angle())
	print(-(robot.angle() % 90))
	#robot.turn(-(robot.angle() % 90))
	startAngle = robot.angle()
	ev3.speaker.say("time for rescue")
	robot.straight(170)
	robot.turn(150)
	robot.drive(0, -40)
	ev3.speaker.beep()
	while True:
		if ultraS.distance() < 500:
			robot.stop()
			print("[" + str(timeSecs.time()) + "]: Capsule detected")
			#gets distance of capsule from robot
			distance = ultraS.distance()
			ev3.speaker.say("Capsule detected")
			#to compensate for distance errors
			sin = 32.5/distance
			turnDistance = asin(sin) * 100 * distance/200
			#print("[" + str(timeSecs.time()) + "]: Turn distance is " + turnDistance)
			robot.turn(-turnDistance) 
			#gets the angle that the robot is turned compared to the starting angle
			angle = startAngle - robot.angle()
			#moves by the distance of the can
			robot.straight(distance * 1/4)
			robot.stop()
			accDistance = ultraS.distance() - 40
			robot.straight(accDistance)
			#opens the claw
			claw.run_angle(180, clawTurn)
			#goes back the distance of the can
			robot.straight(-(distance*1/4 + accDistance))
			robot.turn(angle - turnDistance)
			robot.straight(-180)
			robot.turn(-100)
			robot.straight(100)
			claw.run_angle(180, -clawTurn)
			robot.drive(-driveSpeed, 0)
			while lColor.reflection() > black and rColor.reflection() > black:
				pass
			robot.drive(0, -60)
			while rColor.reflection() > black:
				pass
			robot.stop()
			break
	
	print("[" + str(timeSecs.time()) + "]: Capsule rescued")
	ev3.speaker.say("capsule rescued dad is the best")
			
#Handles all movement
def move():
	while True:
		leftIsBlack = isBlack(lColor)
		rightIsBlack = isBlack(rColor)
		if lColor.reflection() > 90 or rColor.reflection() > 90:
			rescue()
		if (ultraS.distance() < ultraSLimit):
			obstacle(ultraS.distance, turnDriveSpeed)
		#Amount to multiply output by
		compensator = 7
		multiplier = 2.2
		#finds the difference between the reflections
		error = lColor.reflection() - rColor.reflection()
		if leftIsBlack and rightIsBlack:
			robot.stop()

			if lColor.color() == Color.RED or rColor.color() == Color.RED:
				quit()

			doubleGreen1 = (lColor.color == Color.GREEN and rColor.color == Color.GREEN)

			robot.straight(10)

			doubleGreen2 = (lColor.color == Color.GREEN and rColor.color == Color.GREEN)

			if doubleGreen1 and doubleGreen2:
				robot.straight(-20)

			error = lColor.reflection() - rColor.reflection()
			
			if error <= compensator and error >= -compensator:
				robot.drive(turnDriveSpeed, 0)
			elif (lColor.reflection() < rColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
				robot.turn(30)
				robot.straight(50)
				robot.drive(0, 60)
				while lColor.reflection() > black:
					pass
				robot.stop()
				robot.turn(-20)
			elif (lColor.reflection() > rColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
				robot.turn(-30)
				robot.straight(50)
				robot.drive(0, -60)
				while rColor.reflection() > black:
					pass
				robot.stop()
				robot.turn(20)
			else:
				robot.drive(turnDriveSpeed, 0)
		#gets degrees to turn by
		output = int(multiplier * (error))
		#output may need to be limited to within -180, 180
		robot.drive(driveSpeed, output)

def startMessage():
	#Arguments should be 1 and the number of possible outcomes
	rand = random.randint(0, len(helloMessages) - 1)
	ev3.speaker.say(helloMessages[rand])


startMessage()
move()
#test()