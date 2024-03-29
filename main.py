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
import math
import threading
#from math import sqrt, asin

#WHAT IS IN COURSE????
waterTowerCount = 1
rescueCount = 1
whiteLineCount = 0
redLineCount = 0
detourCount = 0
cansCount = 69420
#blackCanCount = 0
blockPos = 0 #changing doesn't do anything
funnyBlok = 0
animalCrossings = 1
animalCrossingsDone = 0
uturn = 0
diversion = 0

# This program requires LEGO EV3 MicroPython v2.0 or higher. (INSTALLED)

#objects
ev3 = EV3Brick()

#sensors
lColor = ColorSensor(Port.S4)
rColor = ColorSensor(Port.S1)
frontColor = ColorSensor(Port.S3)
ultraS = UltrasonicSensor(Port.S2)
ultraSLimit = 90
maxCanDist = 250 #250?
rescueBlockDist = 300
blockMin = 200
blockMax = 300

#motors
lMotor = Motor(Port.C)
rMotor = Motor(Port.B)
claw = Motor(Port.D)
lifter = Motor(Port.A)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55, axle_track=130)
clawTurn = -90

helloMessages = ["Hello there", "Hello mr Dharma", "YOU NILLY SUSAN", "Hello mr Hu", "Uh Will what are you doing", "GET RICKROLLED", "JELLY", "POTATOES", "REFRACTION BEST", "HACK ON 2B2T PLS", "COMMUNISM", "What do you think you are doing", "More start messages means more lag", "JAMES GET OFF MINECRAFT", "yes", "parp", "kathmandu", "what you doing", "hypixel skyblock hype is op", "water tower", "you mrs leech", "you mrs walnut", "hello smoothiedrew", "gas", "andrew's toxic gas", "whale", "scatha", "will is good", "worms", "thats long", "ratfraction is cal but on vape", "rise client is meta", "now for water tower", "wheres the water tower", "laughing", "why are you making so many", "failure", "stop now its too long", "this is smooth", "more start messages means more life", "Jellybean is mid", "FORTNITE BATTLE PASS", "get the ems", "prot 4 bois", "dont waste your money on a subzero wisp PLEASE", "6b9t is best", "nah I don't know what to say", "UR MUM", "it's getting pretty long", "deez nuts are more reflective", "we may need to change some variables", "It should be running the code", "You know what you could add instead? Double rescue", "It's over 9000!", "Dante best"]

#drive speed variables
towerDriveSpeed = 350 #140
driveSpeed = 115 #115 normal 50  small with hills
maxTurnSpeed = 115
a = 0.02
multiplier = 3.2 #so now... #2.5normal 4.2small

#colors
silver = 90
white = 50
black = 25
yellow = 85 #check if small tiles and diversion
#green is 16 - ree

#other variables
rescueComplete = 0 #once completed rescue changes the variable to 1
rescueBlockSize = 300
lastTurn = None
rescueTime = timeSecs.process_time()
startedDetour = False
lastDetour = 0
turningSpeed = 69 #changing doesn't do anything
cansRescued = 0
#program

#Runs if an obstacle is detected
def obstacle(distance):
	robot.stop()
	robot.straight(-10)
	robot.turn(-80)
	robot.drive(towerDriveSpeed, 80)#-distance) #37.5	
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
	#print('isblack')
	if side.reflection() <= black:
		return True
	else:
		return False
	
def isYellow(side):
	if side.reflection() >= yellow - 5 and side.reflection() < yellow + 5:
		return True
	else:
		return False

def doubleWhite(cal):
	print('doublewhite')
	robot.stop()
	iteration = 1

	while not isBlack(lColor) and not isBlack(rColor):
		if iteration == 2:
			move(cal)
		else:
			iteration+=1

		robot.straight(10)
 

def whiteLine(cal):
	print('whiteline')
	robot.stop()

	robot.drive(-25, 0)
	while lColor.reflection() < black and rColor.reflection() < black:
		pass
	robot.stop()

	while lColor.reflection() < black or rColor.reflection() < black:
		if lColor.reflection() < black and rColor.reflection() < black:
			robot.drive(-25,0)
		elif lColor.reflection() < black:
			robot.drive(0,25)
		elif rColor.reflection() < black:
			robot.drive(0,-25)
			
	robot.stop()
	robot.straight(10)

	while True:
		compensator = 2 #Amount to multiply output by
		leftIsBlack = isBlack(lColor)
		rightIsBlack = isBlack(rColor)
		
		diff = lColor.reflection() - rColor.reflection() + cal #finds the difference between the reflections
		if not leftIsBlack and not rightIsBlack:
			doubleWhite(cal)
		output = -int(multiplier * diff) #gets degrees to turn by

		turningSpeed = math.floor(maxTurnSpeed/(abs(a*diff)+1))

  
		print(turningSpeed, ',', output, 'inverted')
  
		robot.drive(turningSpeed, output)
  
def diversionLine(rightYellow, leftYellow, cal):
	print('rightYellow is', rightYellow, ', leftYellow is ', leftYellow)
	robot.stop()
	wait(50)
	robot.straight(15)

	if rightYellow:
		robot.turn(90)
	elif leftYellow:
		robot.turn(-90)
	while frontColor.color() != Color.BLACK:
		diff = lColor.reflection() - rColor.reflection() - cal #finds the difference between the reflections

		output = -int(12 * diff)#\\\\\\\\\+20 #gets degrees to turn by

		turningSpeed = math.floor((maxTurnSpeed/(abs(a*diff)+1))/2)


		print(turningSpeed, ',', output)

		robot.drive(turningSpeed, output)


def redLine():
	global  detourCount, redLineCount, startedDetour, lastDetour
	print('redline')
	robot.straight(10)
	timeSecs.sleep(1)
	robot.stop()

	if frontColor.color() == Color.RED:
		#print("did it get herer?")
		if startedDetour == True:
			#print("what about here")
			if lastDetour == 1:
				robot.drive(100,120)
				timeSecs.sleep(1)#need to change
			#	print('surely')
			elif lastDetour == 2:
				robot.drive(100,-40)
				timeSecs.sleep(1)
			else:
				print("SOMEONE PUT THE WRONG VARS FOR LASTDETOUR, IT SHOULD BE 1 OF 2 (RIGHT/LEFT)")
			startedDetour = False
		elif redLineCount >= 1:
			print('end of line')
			ev3.speaker.beep(69, 420)
			robot.straight(-50)
			wait(20)
			robot.turn(180)
			redLineCount =+ 1


	elif lColor.color() == Color.RED and detourCount >= 1 and startedDetour == False :
		print('right red, going left')
		ev3.speaker.beep(69,69)
		#robot.drive()
		robot.straight(30)
		robot.turn(30)
		wait(20)
		robot.drive(50, 100)
		while rColor.reflection() > 50:
			pass
		robot.stop()
		#robot.drive(0, 40)
		startedDetour = True 
		lastDetour = 1 #left is 1 right is 2

	# Left turn
	elif rColor.color() == Color.RED and detourCount >= 1 and startedDetour == False:
		print("left red, going right")
		ev3.speaker.beep(69,420)
		robot.straight(30)
		robot.turn(-30)
		wait(20)
		robot.drive(50, -100)
		while lColor.reflection() > 50:
			pass
		robot.stop()
		#robot.drive(0, -40)
		startedDetour = True
		lastDetour = 2

	else:
		print('lanond')
		robot.straight(-10)

def AnimalCrossing(cal):
	global animalCrossingsDone

	leftIsBlack = isBlack(lColor)
	rightIsBlack = isBlack(rColor)
	if (animalCrossingsDone == animalCrossings):
		print('canceld')
		return
	elif leftIsBlack == False and rightIsBlack == False:
		robot.straight(-10)
		print('depression')
		return
	

	print('animalcrossing', animalCrossingsDone)
	robot.stop()
	ev3.speaker.beep()
	robot.straight(50)
	ev3.speaker.beep()
	while True:
		diff = lColor.reflection() - rColor.reflection() - cal #finds the difference between the reflections
		
		leftIsBlack = isBlack(lColor)
		rightIsBlack = isBlack(rColor)

		if frontColor.color() == Color.BLUE and leftIsBlack and rightIsBlack:
			print('donewithanimals')
			robot.stop()
			robot.drive(40, 0)
			while lColor.reflection() < black:
				pass
			robot.straight(20)
			wait(20)
			animalCrossingsDone =+ 1
			return
		
		output = int(multiplier * diff) #gets degrees to turn by

		turningSpeed = (math.floor(maxTurnSpeed/(abs(a*diff)+1)))/2

		if turningSpeed <= 10:
			turningSpeed = 10
  
		#print(turningSpeed, ',', output, 'blu')
		robot.drive(turningSpeed, output)

def doubleBlack(compensator, cal):
	print('doubleblack')
	robot.stop
	wait(50)
 
	diff = lColor.reflection() - rColor.reflection()

	iteration = 0

	if detourCount == 1:
		robot.straight(-40)
		if rColor.color() == Color.RED or lColor.color() == Color.RED:
			redLine()
		else:
			robot.straight(40)

	while lColor.reflection() < black and rColor.reflection() < black:
		robot.stop()
		robot.straight(6)

#		if detourCount == 1 and detourDone == 0:
#			if lColor.color == Color.RED or rColor.color() == Color.RED:
#				print('maybe')
#				redLine()
#			robot.straight(-30)


#moana lisa

		if lColor.color() == Color.BLUE and rColor.color() == Color.BLUE and frontColor.color() == Color.BLUE:
			print('AC2')
			AnimalCrossing(cal)

		elif (lColor.color() == Color.GREEN and rColor.color() == Color.GREEN and frontColor.color() == Color.BLACK and uturn == 1):
			print('uturn1')
			robot.straight(-50)
			robot.turn(180)
			return

		#Uncomment for white line
		iteration += 1
		if iteration >= 3 and whiteLineCount == 1:
			#checkGreenCol()
			whiteLine(cal)

		if diff <= 2 and diff >= -2:
			print(' pass')

		# Right turn
		if (lColor.reflection() < rColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
			print('right1')
			robot.turn(10) #10 small 15 normal
			robot.drive(100, 0)
			while lColor.reflection() < black:
				pass
			robot.stop()
			robot.drive(0, 40)

		# Left turn
		elif (rColor.reflection() < lColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
			print('left1')
			robot.turn(-10) #10 small 15 normal??
			robot.drive(100, 0)
			while rColor.reflection() < black:
				pass
			robot.stop()
			robot.drive(0, -40)

		elif frontColor.color() ==Color.GREEN and rColor.reflection() > 99 and lColor.reflection() > 99:
			rescueTime = rescue()

		elif diff <= 2 and diff >= -2:
			print(' pass')

		else:
			print('bruh2')

def checkGreenCol():
	print('bruh')

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
		robot.turn(-20) #15 small 25 normal??
		robot.drive(100, 0)
		while rColor.reflection() < black:
			pass
		robot.stop()
		robot.drive(0, -40)
	elif(rColor.color() == Color.GREEN):
		robot.turn(20) #15 small 25 normal
		robot.drive(100, 0)
		while lColor.reflection() < black:
			pass
		robot.stop()
		robot.drive(0, 40)
	else:
		return
	
def centerRescue():
	robot.drive(-25, 0)
	while lColor.reflection() >= 97 or rColor.reflection() >= 97:
		pass
	robot.stop()

	while lColor.reflection() < 97 or rColor.reflection() < 97:
		if lColor.reflection() < 97 and rColor.reflection() < 97:
			robot.drive(25, 0)
		elif lColor.reflection() < 97:
			robot.drive(0, 25)
		else:
			robot.drive(0,-25)



def rescue():
	global rescueCount, blockPos, cansRescued, maxCanDist, rescueBlockDist
 
	cansRescued = 0
	print('rescueee')
	robot.stop()
	claw.run_angle(-200, 50)

	centerRescue()

	startAngle = robot.angle()
 
	#maxCanDist = 250
	#blockDist = 270
 
	wait(20)
	robot.straight(220)
	wait(20)
	if funnyBlok == 0:
		robot.turn(-30)
	
	wait(10)
	
	while (startAngle - robot.angle()) < 360:
		robot.drive(0, -40)
		if ultraS.distance() < maxCanDist:
			canDist = ultraS.distance()
			robot.stop()
			wait(50)
		
			#finds center of can
			robot.turn(-20)

			robot.drive(0,-15)#small turn
			while ultraS.distance() < maxCanDist:
				pass
			robot.stop()
			canRight = robot.angle()
			ev3.speaker.beep()
			robot.turn(20)

			robot.drive(0,25)
			wait(50)
			while ultraS.distance() > maxCanDist: #turn untill sees can again
				pass
			robot.stop()

			robot.drive(0,25)
			while ultraS.distance() < maxCanDist:
				pass
			robot.stop()
			canLeft = robot.angle()
			ev3.speaker.beep()
			#calc center here
			canCompensation = canRight - canLeft
			print(canRight,canLeft,canCompensation,canDist)
			robot.turn(canCompensation/2)
			wait(20)
			canDist = ultraS.distance()

			print(canDist)

			#if canCompensation >= 100 or canCompensation <= -100:
			#	return
			if canDist <= 50:
				robot.straight(canDist - 20)
			else:
				robot.straight(canDist - 50)
			ev3.speaker.beep()
			robot.stop()
			wait(20)

		
			lifter.run_angle(100,90,wait=True)
			wait(20)
			robot.straight(45)
			
			claw.run_time(100,1000,wait=True) #centers it with claw
			claw.run_time(100,100,wait=True) #reopens claw
			claw.stop()
			robot.straight(10) #might knock can over
			claw.run(100) #grabs can
			wait(200)
			#robot.straight(-12)
			#wait(20)
			lifter.run_angle(95,-90,wait=True) #lifts can
			#robot.straight(14)
			if canDist <= 50:
				robot.straight(-(canDist - 30))
			else:
				robot.straight(-(canDist+5)) #back to middle

			robot.turn((startAngle-robot.angle())) #face block
			robot.stop()
			if funnyBlok == 1 and cansRescued == 0:
				wait(100)
				if ultraS.distance() <= blockMax and ultraS.distance() >= blockMin:
					blockPos = 0
				else:
					wait(20)
					robot.turn(90)
					wait(100)
					if ultraS.distance() <= blockMax and ultraS.distance() >= blockMin:
						blockPos = 90
					else:
						wait(20)
						robot.turn(-180)
						wait(100)
						if ultraS.distance() <= blockMax and ultraS.distance() >= blockMin:
							blockPos = -90
						else:
							pass #sys.exit()
			else:
				pass


			robot.straight(rescueBlockDist-41) #goto block
				
			lifter.run_angle(30,20) #lower lifter
			wait(100)
			claw.stop()
			claw.run_angle(-100,50,wait=True) #drop can
			lifter.run_angle(30,-20)
			robot.straight(-rescueBlockDist+21)
			cansRescued =+1
			robot.turn(-blockPos)
			robot.turn(-30)

	if funnyBlok == 1:
		if blockPos == 0:
			robot.turn(180)
		else:
			robot.turn(blockPos)
	else:
		robot.turn(180)

	robot.drive(100, 0)
	while lColor.reflection() < 70:
		pass
	robot.stop()
	robot.straight(20)
	lifter.run_until_stalled(200)
	claw.run_angle(50, 50)
	lifter.run_angle(100,-90)
					


	#robot.turn(150)
	robot.straight(20)

	robot.drive(0, 90)
	while lColor.reflection() > black:
		pass

	robot.stop()
	robot.turn(-30)
	robot.straight(20)

	rescueCount -= 1

	return timeSecs.process_time() + 5
def checkRescue():
	print('check!', frontColor.color())
	testDist = 20
	robot.stop()
	#robot.straight(testDist)
	if frontColor.color() == Color.BLUE or frontColor.color() == Color.GREEN or frontColor.color() == Color.BLACK:
		#robot.drive(-10,0)
		robot.straight(-testDist)
		#robot.straight(-10)
		rescueTime = rescue()
	else:
		robot.straight(-testDist)
		rescueTime = timeSecs.process_time() + 0.1
	return rescueTime

#Handles all movement
def move(cal):
	global multiplier
	robot.stop()
	rescueTime = timeSecs.process_time()
	#ev3.speaker.beep()
	while True:
		compensator = 2 #Amount to multiply output by
		leftIsBlack = isBlack(lColor)
		rightIsBlack = isBlack(rColor)
		if rescueCount >= 1:
			if lColor.reflection() > 99 or rColor.reflection() > 99:
				if timeSecs.process_time() < rescueTime:
					pass
				else:
					rescueTime = checkRescue()
		if waterTowerCount >= 1:
			if (ultraS.distance() < ultraSLimit):
				obstacle(ultraS.distance())
		diff = lColor.reflection() - rColor.reflection() - cal #finds the difference between the reflections
		
		if diversion >= 1:
			rightYellow = isYellow(rColor)
			leftYellow = isYellow(lColor)

			if rightYellow or leftYellow:
				diversionLine(rightYellow, leftYellow, cal)

		if frontColor.color() == Color.RED and (redLineCount >= 1 or detourCount >=1): #between -10 and 10
			redLine()

		if frontColor.color() == Color.BLUE and animalCrossings == 1 and leftIsBlack and rightIsBlack:
			AnimalCrossing(cal)

		if leftIsBlack and rightIsBlack:
			doubleBlack(compensator, cal)
	
		output = int(multiplier * diff) #gets degrees to turn by

		turningSpeed = math.floor(maxTurnSpeed/(abs(a*diff)+1))
		#turningSpeed = math.floor(math.sqrt(10000-diff*diff))
  
		#print(turningSpeed, ',', output, 'normal')
		robot.drive(turningSpeed, output)
		
def startMessage():
	ev3.speaker.set_speech_options(voice="m7")
	ev3.speaker.set_volume(10000)
	#Arguments should be 1 and the number of possible outcomes
	rand = random.randint(0, len(helloMessages) - 1)
	ev3.speaker.say(helloMessages[rand])

def cal():
	dif = lColor.reflection() - rColor.reflection() #- frontColor.reflection()
	return dif

def initiate():
	#startMessage()
	lifter.run_angle(100,-90, wait=False)
	claw.run_until_stalled(100)
	#ev3.speaker.say("Close the claw you nons")
	ev3.speaker.beep()
	while len(ev3.buttons.pressed()) == 0:
		pass
	dif = cal()
	print(dif)
	wait(200)
	ev3.speaker.beep()
	while len(ev3.buttons.pressed()) == 0:
		pass

	ev3.speaker.beep(200,20)

	move(dif)


def test():
	#initiate()
	while True:
		print(ultraS.distance())
	while True:
		diff = lColor.reflection() - rColor.reflection() - cal #finds the difference between the reflections
  
		output = int(multiplier * diff) #gets degrees to turn by
  
		print(lColor.reflection(), rColor.reflection(), output, diff)

		#turningSpeed = -(a * output)**2 + maxTurnSpeed
		turningSpeed = -math.floor((a * output)** 2 + maxTurnSpeed)
  
		print(turningSpeed)
  
		if turningSpeed < 15:
			turningSpeed = 15
  
		print(turningSpeed)
  
		wait(100)
  
		robot.drive(turningSpeed, output)

#test()
#funnythread.start()
initiate()
#landon()