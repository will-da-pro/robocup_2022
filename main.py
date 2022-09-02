#!/usr/bin/env pybricks-micropython
import sys
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor, Motor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time as timeSecs
import random
from math import sqrt, asin
import threading

# This program requires LEGO EV3 MicroPython v2.0 or higher. (INSTALLED)

#objects
ev3 = EV3Brick()

#sensors
lColor = ColorSensor(Port.S1)
rColor = ColorSensor(Port.S4)
ultraS = UltrasonicSensor(Port.S3)
ultraSLimit = 50

#motors
lMotor = Motor(Port.A)
rMotor = Motor(Port.D)
claw = Motor(Port.B)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55, axle_track=130) #fixed
clawTurn = 200

#drive speed variables
driveSpeed = 125 #125 normal  75 small
turnDriveSpeed = 60
towerDriveSpeed = 180

#colors
silver = 90
white = 50
black = 25
green1 = 12
green2 = 20
red = 65

#other variables
rescueComplete = 0 #once completed rescue changes the variable to 1
lastTurn = None
ev3.speaker.set_volume(50000) #why...

#program

#Runs if an obstacle is detected
def obstacle(distance, speed):
	robot.stop()
	robot.straight(-40)
	robot.turn(-80)
	robot.drive(towerDriveSpeed, 58)	
	wait(300)
	while not isBlack(lColor) and not isBlack(rColor):
		pass
	robot.turn(-50)
	robot.straight(10)
	robot.turn(-20)
			
def isBlack(side):
	if side.reflection() <= black:
		return True
	else:
		return False

def isWhite(side):
	if side.reflection() >= black:
		return True
	else:
		return False

def doubleBlack(compensator):
	robot.stop()
	robot.straight(10)

	error = lColor.reflection() - rColor.reflection()

	iteration = 0
	
	while lColor.reflection() < black and rColor.reflection() < black:
		iteration += 1

		if iteration >= 3:
			whiteLine()

		if error <= compensator and error >= -compensator:
			pass

		# Right turn
		elif (lColor.reflection() < rColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
			robot.turn(25)
			robot.drive(60, 0)
			while lColor.reflection() < black:
				pass
			robot.stop()
			robot.drive(0, 40)

		# Left turn
		elif (rColor.reflection() < lColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
			robot.turn(-25)
			robot.drive(60, 0)
			while rColor.reflection() < black:
				pass
			robot.stop()
			robot.drive(0, -40)

		else:
			pass

def doubleWhite(compensator):
	iteration = 0
	
	while lColor.reflection() > black and rColor.reflection() > black:
		robot.stop()
		robot.straight(10)

		error = rColor.reflection() - lColor.reflection()

		iteration += 1

		if iteration >= 3:
			move()

def rescue():
	robot.stop()
	wait(100)
	print(robot.angle())
	#robot.turn(-(robot.angle() % 90))
	startAngle = robot.angle()
	robot.straight(170)
	robot.turn(120)
	robot.drive(0, -40)
	while ultraS.distance() > 500:
		pass

	ev3.speaker.beep()

	canStartAngle = robot.angle()

	while ultraS.distance() < 500:
		pass

	robot.stop()

	ev3.speaker.beep()

	canEndAngle = robot.angle()

	robot.turn((canStartAngle - canEndAngle)/2)

	distance = ultraS.distance()
	angle = startAngle - robot.angle() #to compensate for distance errors
	robot.straight(distance) #moves by the distance of the can
	robot.stop()
	#accDistance = ultraS.distance()
	#robot.straight(accDistance)
	claw.run_angle(400, clawTurn) 	#closes the claw

	canDist = robot.distance()
	robot.drive(100, 0)
	while lColor.reflection() <= 30 and rColor.reflection() <= 30:
		pass

	robot.stop()

	robot.straight(20)

	claw.run_angle(400, -clawTurn)

	robot.straight(-20)

	robot.straight(canDist - robot.distance())

	#goes back the distance of the can
	robot.straight(-(distance))
	robot.turn(angle)
	robot.straight(-180)

	#robot.stop()
	robot.turn(60)

	robot.drive(0, 75)
	while lColor.reflection() > black:
		pass

	robot.stop()

	rescueComplete = 1
			

def whiteLine():
	ev3.speaker.beep()
	print("whiteLine")
	while True:
		leftIsWhite = isWhite(lColor)
		rightIsWhite = isWhite(rColor)
		if lColor.reflection() > 99 or rColor.reflection() > 99:
			if rescueComplete == 1:
				pass
			else:
				rescue()
		if (ultraS.distance() < ultraSLimit):
			obstacle(ultraS.distance, turnDriveSpeed)
		compensator = 2 #Amount to multiply output by
		multiplier = 4
		error = rColor.reflection() - lColor.reflection() #finds the difference between the reflections
		if leftIsWhite and rightIsWhite:
			doubleWhite(compensator)
		if lColor.reflection() < red and lColor.reflection() > black and rColor.reflection() < red and rColor.reflection() > black:
			redLine()
		output = int(multiplier * error) #gets degrees to turn by
		robot.drive(driveSpeed, output) #output may need to be limited to within -180, 180 (?)

def redLine():
	robot.stop()
	if (lColor.color() == Color.RED or rColor.color() == Color.RED):
		sys.exit()

#Handles all movement
def move():
	ev3.speaker.beep()
	while True:
		compensator = 2 #Amount to multiply output by
		leftIsBlack = isBlack(lColor)
		rightIsBlack = isBlack(rColor)
		if lColor.reflection() > 99 or rColor.reflection() > 99:
			if rescueComplete == 1:
				pass
			else:
				rescue()
		if (ultraS.distance() < ultraSLimit):
			obstacle(ultraS.distance, turnDriveSpeed)
		multiplier = 7
		error = lColor.reflection() - rColor.reflection() #finds the difference between the reflections
		if leftIsBlack and rightIsBlack:
			doubleBlack(compensator)
		if lColor.reflection() < red and lColor.reflection() > black and rColor.reflection() < red and rColor.reflection() > black:
			redLine()
		output = int(multiplier * error) #gets degrees to turn by
		robot.drive(driveSpeed, output) #output may need to be limited to within -180, 180 (?)

def test():
	while True:
		#ev3.screen.print(ultraS.distance())
		ev3.screen.print(str(lColor.color()) + ", " + str(rColor.color()))

#testThread = threading.Thread(target=test)
#testThread.start()
#test()
move()
