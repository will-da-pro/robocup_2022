#!/usr/bin/env pybricks-micropython
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
driveSpeed = 75 #125 normal  75 small
turnDriveSpeed = 60
towerDriveSpeed = 180

#colors
silver = 90
white = 50
black = 20
green1 = 12
green2 = 20

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
	wait(30)
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

def rescue():
	robot.stop()
	wait(100)
	print(robot.angle())
	print(-(robot.angle() % 90))
	#robot.turn(-(robot.angle() % 90))
	startAngle = robot.angle()
	robot.straight(170)
	robot.turn(120)
	robot.drive(0, -40)
	ev3.speaker.beep()

	while ultraS.distance() > 500:
		pass

	startAngle2 = robot.angle()
	endAngle = robot.angle()
	robot.stop()
	turnDistance = (startAngle2 - endAngle) / 2
	robot.turn(turnDistance) 
	distance = ultraS.distance() #gets distance of capsule from robot
	robot.turn(-15)
	angle = startAngle - robot.angle() #to compensate for distance errors
	robot.straight(distance * 1/4) #moves by the distance of the can
	robot.stop()
	accDistance = ultraS.distance()
	robot.straight(accDistance)
	claw.run_angle(400, clawTurn) 	#closes the claw

	canDist = robot.distance()
	robot.drive(100, 0)
	while lColor.reflection() <= 30 and rColor.reflection() <= 30:
		pass

	robot.stop()

	claw.run_angle(400, -clawTurn)

	robot.straight(canDist - robot.distance())

	#goes back the distance of the can
	robot.straight(-(distance*1/4 + accDistance))
	robot.turn(angle - turnDistance)
	robot.straight(-180)
	robot.drive(0, 50)
	while lColor.reflection() > black:
		pass

	robot.stop()

	rescueComplete = 1
			
#Handles all movement
def move():
	while True:
		leftIsBlack = isBlack(lColor)
		rightIsBlack = isBlack(rColor)
		if lColor.reflection() > 95 or rColor.reflection() > 98:
			if rescueComplete == 1:
				pass
			else:
				rescue()
		if (ultraS.distance() < ultraSLimit):
			obstacle(ultraS.distance, turnDriveSpeed)
		#Amount to multiply output by
		compensator = 2
		multiplier = 3 #2.5 normal  2.8 small
		
		#finds the difference between the reflections
		error = lColor.reflection() - rColor.reflection()
		if leftIsBlack and rightIsBlack:
			robot.stop()
			robot.straight(10)

			error = lColor.reflection() - rColor.reflection()
			
			if error <= compensator and error >= -compensator:
				robot.drive(driveSpeed, 0)
			#	print (lastTurn)
			#	if lastTurn == 0:
			#		error = -1000
			#	else:
			#		error = 1000

			elif (lColor.reflection() < rColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
				robot.turn(30)
				robot.straight(60)
				robot.drive(0, 40)
			elif (rColor.reflection() < lColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
				robot.turn(-30)
				robot.straight(60)
				robot.drive(0, -40)
			else:
				robot.drive(turnDriveSpeed, 0)
		output = int(multiplier * error) #gets degrees to turn by

		if error <= compensator and error >= -compensator:
			error = 0

		if output < 0:
			lastTurn = 0
		else:
			lastTurn = 1
		robot.drive(driveSpeed, output) #output may need to be limited to within -180, 180 (?)

def test():
	while True:
		ev3.speaker.beep(ultraS.distance(), 1)
		ev3.screen.print(ultraS.distance())
		#ev3.screen.print(str(lColor.reflection()) + ", " + str(rColor.reflection()))

#testThread = threading.Thread(target=test)
#testThread.start()
#test()
move()
