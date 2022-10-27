#!/usr/bin/env pybricks-micropython
import random
import sys
from timeit import repeat
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor, Motor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time as timeSecs
#from math import sqrt, asin
import threading

# This program requires LEGO EV3 MicroPython v2.0 or higher. (INSTALLED)

#objects
ev3 = EV3Brick()

#sensors
lColor = ColorSensor(Port.S4)
rColor = ColorSensor(Port.S1)
frontColor = ColorSensor(Port.S2)
ultraS = UltrasonicSensor(Port.S3)
ultraSLimit = 100
maxCanDist = 400
rescueBlockDist = 300

#motors
lMotor = Motor(Port.D)
rMotor = Motor(Port.A)
claw = Motor(Port.B)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55, axle_track=130) #fixed
clawTurn = 400

#drive speed variables
driveSpeed = 115 #115 normal  85 small
turnDriveSpeed = 60
towerDriveSpeed = 280 #140

#colors
silver = 90
white = 50
black = 25
green1 = 12
green2 = 20
red = 65

#other variables
rescueComplete = 0 #once completed rescue changes the variable to 1
rescueBlockSize = 300
lastTurn = None
rescueTime = timeSecs.process_time()

#program

#Runs if an obstacle is detected
def obstacle(distance, speed):
	robot.stop()
	robot.straight(-10)
	robot.turn(-80)
	robot.drive(towerDriveSpeed, 75) #37.5	
	wait(300)
	while not isBlack(lColor) and not isBlack(rColor):
		pass
	robot.drive(-50, 0)
	while lColor.reflection() > black and rColor.reflection() > black:
		pass
	robot.stop()
	robot.turn(-50)
	robot.straight(20)
	robot.turn(-20)
			
def isBlack(side):
	if side.reflection() <= black:
		return True
	else:
		return False

def doubleBlack(compensator):

	wait(50)

	diff = lColor.reflection() - rColor.reflection()

	iteration = 0
	
	while lColor.reflection() < black and rColor.reflection() < black:
		robot.stop()
		robot.straight(7.5)

		#Uncomment for white line
		iteration += 1
		if iteration >= 2:
			checkGreenCol()
		#	if iteration >= 10:
		#		robot.drive(10000000, 0)
		#		while True:
		#			pass
		#	whiteLine()

		if diff <= compensator and diff >= -compensator:
			pass

		# Right turn
		elif (lColor.reflection() < rColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
			robot.turn(15) #10 small 15 normal
			robot.drive(100, 0)
			while lColor.reflection() < black:
				pass
			robot.stop()
			robot.drive(0, 40)

		# Left turn
		elif (rColor.reflection() < lColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
			robot.turn(-15)
			robot.drive(100, 0)
			while rColor.reflection() < black:
				pass
			robot.stop()
			robot.drive(0, -40)

		else:
			pass

def checkGreenCol():
	if lColor.color() == Color.GREEN and rColor.color() == Color.GREEN:
		robot.straight(-15)
		rescueTime = rescue()
	if(lColor.color() == Color.GREEN):
		robot.turn(-15)
		robot.drive(100, 0)
		while rColor.reflection() < black:
			pass
		robot.stop()
		robot.drive(0, -40)
	elif(rColor.color() == Color.GREEN):
		robot.turn(15) #15 small 25 normal
		robot.drive(100, 0)
		while lColor.reflection() < black:
			pass
		robot.stop()
		robot.drive(0, 40)
	else:
		return

def rescue():
	robot.stop()
	rescueBlock = 0
	wait(100)
	claw.run_until_stalled(-clawTurn)
	print(robot.angle())
	#robot.turn(-(robot.angle() % 90))
	startAngle = robot.angle()
	robot.straight(120)
	robot.turn(120)

	turnStopDist = robot.angle() - 240
	rescueObjs = []
	detectedObjs = []
	lastDist = ultraS.distance()
	minLengthDif = 500
	maxUltraSDist = 400
	objStartAngle = 0
	objEndAngle = 0
	
	robot.drive(0, -60)

	while robot.angle() >= turnStopDist:
		dist = ultraS.distance()

		if dist > maxUltraSDist:
			if len(detectedObjs) > 0:
				for x in rescueObjs:
					#ev3.speaker.beep()

					objEndAngle = robot.angle()
					objSize = objEndAngle - objStartAngle
					objMidPoint = objStartAngle + (objStartAngle - objEndAngle)/2 - 20

					if objStartAngle < startAngle and objEndAngle > startAngle:
						rescueBlock = [objSize, objMidPoint, dist]
					else:
						rescueObjs.append([objSize, objMidPoint, dist])
						robot.drive(0, -60)
		if dist - lastDist >= minLengthDif:
			ev3.speaker.beep()

			print("start" + str(dist) + ", " + str(lastDist))
			
			detectedObjs.append(dist)
			objStartAngle = robot.angle()
		elif lastDist - dist >= minLengthDif:
			ev3.speaker.beep()

			print("end" + str(dist) + ", " + str(lastDist))
			objEndAngle = robot.angle()
			objSize = objEndAngle - objStartAngle
			objMidPoint = objStartAngle + (objStartAngle - objEndAngle)/2 - 20

			if objStartAngle < startAngle and objEndAngle > startAngle:
				rescueBlock = [objSize, objMidPoint, dist]
			else:
				rescueObjs.append([objSize, objMidPoint, dist])
				robot.drive(0, -60)
		lastDist = dist

	print(rescueObjs)

	if len(rescueObjs) < 1:
		robot.turn(startAngle - robot.angle())

		distance = ultraS.distance()
		angle = startAngle - robot.angle() #to compensate for distance diffs
		robot.straight(distance) #moves by the distance of the can
		robot.stop()

		if (frontColor.reflection() < 99):
			claw.run_until_stalled(clawTurn) 	#closes the claw
			claw.hold()

			robot.straight(-distance)
		else:
			print("Can not found")
		
	else:
		for x in rescueObjs:
			robot.turn(x[1] - robot.angle())

			distance = ultraS.distance()
			angle = startAngle - robot.angle() #to compensate for distance diffs
			robot.straight(distance) #moves by the distance of the can
			robot.stop()

			if (frontColor.reflection() < 99):
				claw.run_until_stalled(clawTurn) 	#closes the claw
				claw.hold()

				robot.straight(-distance)

	robot.turn(rescueBlock[1] - robot.angle())
	#accDistance = ultraS.distance()
	#robot.straight(accDistance)

	robot.straight(rescueBlock[2])

	claw.run_until_stalled(-clawTurn)

	robot.straight(-rescueBlock[2])

	#robot.stop()
	robot.turn(150)

	robot.drive(0, 75)
	while lColor.reflection() > black:
		pass

	robot.stop()

	robot.turn(-30)

	robot.straight(20)

	rescueComplete = 1
	claw.run_until_stalled(clawTurn)
	claw.hold()
	claw.run_angle(100, -100)

	return timeSecs.process_time() + 50

def checkRescue():
	robot.stop()
	robot.straight(50)
	if lColor.reflection() < black and rColor.reflection() < black:
		rescueTime = rescue()
	else:
		robot.straight(-50)
		rescueTime = timeSecs.process_time() + 0.1
	return rescueTime

def redLine():
	robot.stop()
	wait(300)
	robot.straight(5)
	if (lColor.color() == Color.RED or rColor.color() == Color.RED):
		sys.exit()

#Handles all movement
def move():
	robot.stop()
	rescueTime = timeSecs.process_time()
	ev3.speaker.beep()
	while True:
		compensator = 2 #Amount to multiply output by
		leftIsBlack = isBlack(lColor)
		rightIsBlack = isBlack(rColor)
		if lColor.reflection() > 99 or rColor.reflection() > 99:
			if timeSecs.process_time() < rescueTime:
				pass
			else:
				rescueTime = checkRescue()
		#if (ultraS.distance() < ultraSLimit):
		#	obstacle(ultraS.distance, turnDriveSpeed)
		multiplier = 3 #2.5normal 4.7small
		diff = lColor.reflection() - rColor.reflection() #finds the difference between the reflections
		if leftIsBlack and rightIsBlack:
			doubleBlack(compensator)
		#Uncomment for redline
		#if lColor.reflection() < red and lColor.reflection() > black and rColor.reflection() < red and rColor.reflection() > black:
		#	redLine()
		#	pass
		output = int(multiplier * diff) #gets degrees to turn by
		robot.drive(driveSpeed, output) #output may need to be limited to within -180, 180 (?)


def initiate():
	ev3.speaker.say("Close the claws")
	#claw.run_until_stalled(100)
	ev3.speaker.beep()
	#ev3.speaker.play_file("rickroll.alsa")
	while len(ev3.buttons.pressed()) == 0:
		pass
	move()
def test():
	while True:
		ev3.screen.print(str(lColor.color()) + ", " + str(rColor.color()))

#testThread = threading.Thread(target=test)
#testThread.start()


#test()
initiate()