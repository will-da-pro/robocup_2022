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
frontColor = ColorSensor(Port.S3)
ultraS = UltrasonicSensor(Port.S2)
ultraSLimit = 100
maxCanDist = 400
rescueBlockDist = 300

#motors
lMotor = Motor(Port.C)
rMotor = Motor(Port.B)
claw = Motor(Port.D)
lifter = Motor(Port.A)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55, axle_track=130) #fixed
clawTurn = -90

helloMessages = ["Hello there", "Hello mr Dharma", "YOU NILLY SUSAN", "Hello mr Hu", "GET RICKROLLED", "JELLY", "POTATOES", "REFRACTION BEST", "HACK ON 2B2T PLS", "COMMUNISM", "What do you think you are doing", "More start messages means more lag", "yes", "parp", "kathmandu", "what you doing", "hypixel skyblock hype is op", "water tower", "you mrs leech", "you mrs walnut", "hello smoothiedrew", "gas", "andrew's toxic gas", "whale", "scatha", "will is good", "worms", "thats long", "ratfraction is cal but on vape", "rise client is meta", "now for water tower", "wheres the water tower", "laughing", "why are you making so many", "failure", "stop now its too long", "this is smooth", "more start messages means more life", "Jellybean is mid", "FORTNITE BATTLE PASS", "get the ems", "prot 4 bois", "dont waste your money on a subzero wisp PLEASE", "6b9t is best", "nah I don't know what to say", "UR MUM", "it's getting pretty long", "Mike Oxlong", "Kimmy Head", "deez nuts are more reflective", "we may need to change some variables", "It should be running the code", "You know what you could add instead? Double rescue"]

#drive speed variables
driveSpeed = 115 #115 normal  85 small
turnDriveSpeed = 60
towerDriveSpeed = 280 #140

#colors
silver = 90
white = 50
black = 30
green1 = 12
green2 = 25
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

	robot.stop
	wait(50)
 
	diff = lColor.reflection() - rColor.reflection()

	iteration = 0
 
	uTurn = (lColor.reflection() + rColor.reflection())/2
 
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

		#if diff <= compensator and diff >= -compensator:
		#	pass


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
		robot.straight(30)
		print('2green')
		if lColor.color() == Color.BLACK and rColor.color() == Color.BLACK:
			robot.turn(180)
			print('180')
   # move back to check silver??
		elif lColor.color() == Color.GREEN and rColor.color() == Color.GREEN:
			robot.turn(-15)
			rescueTime = rescue()
   
		else:
			pass

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
 
	maxCanDist = 300
	blockDist = 270
 
	wait(100)
	robot.straight(220)
	robot.drive(0,-100)
	while ultraS.distance() < maxCanDist:
		pass
	robot.stop()
	wait(50)
	claw.run_angle(-200, 50)
 
	startAngle = robot.angle()
 
	robot.drive(0, -20)
 
	while robot.angle() - startAngle < 300:
		if ultraS.distance() < maxCanDist:
			canDist = ultraS.distance()
			robot.stop()
			wait(1000)

			blockMax = 300
			blockMin = 200
			#check if orange
			#while canDist < blockMax and canDist > blockMin and (robot.angle() - startAngle) < 130 and (robot.angle() - startAngle) > 170:
			#	robot.drive(0,20)#change
			#robot.stop()
			#wait(10)

			#finds center of can
			robot.drive(0,-20)
			while ultraS.distance() < maxCanDist:
				pass
			robot.stop()
			canRight = robot.angle()
			ev3.speaker.beep()

			robot.drive(0,20)
			while ultraS.distance() > maxCanDist: #turn untill sees can again
				pass
			robot.stop()

			robot.drive(0,20)
			while ultraS.distance() < maxCanDist:
				pass
			robot.stop()
			canLeft = robot.angle()
			ev3.speaker.beep()
			#calc center here
			canCompensation = canRight - canLeft
			print(canRight,canLeft,canCompensation,canDist)
			robot.turn(canCompensation/2)
			
			robot.straight(canDist - 30)
			ev3.speaker.beep()
			robot.stop()
			wait(20)
			robot.straight(-75)
   
			if frontColor.color() == Color.RED or frontColor.reflection() < 2:
				robot.straight(-(canDist - 30))
				robot.turn(-20)#change this if going forward again
				robot.drive(0, -20)
			else:
				wait(1000)
				lifter.run_angle(100, -90,wait=True)
				robot.straight(-(canDist-55))
				robot.turn((startAngle-robot.angle())%360)
				robot.straight(blockDist)
				lifter.run_angle(30,20)
				wait(750)
				claw.stop()
				claw.run_angle(-100,50,wait=True)
				robot.straight(-450)
				lifter.run_until_stalled(200)
				lifter.run_angle(100,-90)
				claw.run_angle(200, 50,wait=True)

def checkRescue():
	testDist = 50
	robot.stop()
	robot.straight(testDist)
	if lColor.reflection() < black and rColor.reflection() < black:
		robot.drive(-10,0)
		robot.straight(-testDist)
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
		if (ultraS.distance() < ultraSLimit):
			obstacle(ultraS.distance, turnDriveSpeed)
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


def startMessage():
	ev3.speaker.set_speech_options(voice="m7")
	ev3.speaker.set_volume(100)
	#Arguments should be 1 and the number of possible outcomes
	rand = random.randint(0, len(helloMessages) - 1)
	ev3.speaker.say(helloMessages[rand])

def initiate():
	#startMessage()
	lifter.run_angle(100,-90)
	claw.run_until_stalled(50)
	#ev3.speaker.say("Close the claw you nons")
	ev3.speaker.beep()
	#while len(ev3.buttons.pressed()) == 0:
	#	pass
	move()


def test():
	lifter.run_angle(100,-20)#up
	wait(5000)
	claw.run(100)#close
	wait(3000)
	lifter.run_angle(100,-70)#up more
	wait(1000)



#testThread = threading.Thread(target=test)
#testThread.start()

#test()
initiate()
