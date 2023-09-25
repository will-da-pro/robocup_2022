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
waterTowerCount = 0
rescueCount = 2
whiteLineCount = 0
detourCount = 0
redLineCount = 0
blueLineCount = 0
cansCount = 10
#blackCanCount = 0
blockPos = 0 #changing doesn't do anything
funnyBlok = 0

# This program requires LEGO EV3 MicroPython v2.0 or higher. (INSTALLED)

#objects
ev3 = EV3Brick()

#sensors
lColor = ColorSensor(Port.S4)
rColor = ColorSensor(Port.S1)
frontColor = ColorSensor(Port.S3)
ultraS = UltrasonicSensor(Port.S2)
ultraSLimit = 90
maxCanDist = 400
rescueBlockDist = 300

#motors
lMotor = Motor(Port.C)
rMotor = Motor(Port.B)
claw = Motor(Port.D)
lifter = Motor(Port.A)
robot = DriveBase(lMotor, rMotor, wheel_diameter=55, axle_track=130) #fixed
clawTurn = -90

helloMessages = ["Hello there", "Hello mr Dharma", "YOU NILLY SUSAN", "Hello mr Hu", "Uh Will what are you doing", "GET RICKROLLED", "JELLY", "POTATOES", "REFRACTION BEST", "HACK ON 2B2T PLS", "COMMUNISM", "What do you think you are doing", "More start messages means more lag", "JAMES GET OFF MINECRAFT", "yes", "parp", "kathmandu", "what you doing", "hypixel skyblock hype is op", "water tower", "you mrs leech", "you mrs walnut", "hello smoothiedrew", "gas", "andrew's toxic gas", "whale", "scatha", "will is good", "worms", "thats long", "ratfraction is cal but on vape", "rise client is meta", "now for water tower", "wheres the water tower", "laughing", "why are you making so many", "failure", "stop now its too long", "this is smooth", "more start messages means more life", "Jellybean is mid", "FORTNITE BATTLE PASS", "get the ems", "prot 4 bois", "dont waste your money on a subzero wisp PLEASE", "6b9t is best", "nah I don't know what to say", "UR MUM", "it's getting pretty long", "deez nuts are more reflective", "we may need to change some variables", "It should be running the code", "You know what you could add instead? Double rescue", "It's over 9000!", "Dante best"]

#drive speed variables
towerDriveSpeed = 280 #140
driveSpeed = 115 #115 normal 50  small with hills
maxTurnSpeed = 115
turningSpeed = 69 #changing doesn't do anything
a = 0.02
multiplier = 3.5 #2.5normal 4.2small

#colors
silver = 90
white = 50
black = 30
green1 = 12
green2 = 25
redA = 50
redB = 35

#other variables
rescueComplete = 0 #once completed rescue changes the variable to 1
rescueBlockSize = 300
lastTurn = None
rescueTime = timeSecs.process_time()
detourDone = 0

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

def doubleWhite(cal):
	print('doublewhite')
	robot.stop
	wait(50)
 
	diff = lColor.reflection() - rColor.reflection()

	iteration = 0
 
 
	while lColor.reflection() > black and rColor.reflection() > black:
		robot.stop()
		robot.straight(7.5)

		iteration += 1
		if iteration >= 2:
			checkGreenCol()
			move(cal)

def whiteLine(cal):
	print('whiteline')
	robot.stop()
	if blueLineCount >=1:
		if lColor.color() == Color.BLUE and rColor.color() == Color.BLUE:
			robot.straight(50)
			while lColor.color() != Color.BLUE and rColor.color() != Color.BLUE:
				diff = lColor.reflection() - rColor.reflection() + cal
				output = int(multiplier * diff) #gets degrees to turn by
				turningSpeed = math.floor(maxTurnSpeed/(abs(a*diff)+1))-60
				if turningSpeed <= 10:
					turningSpeed = 10
				print(turningSpeed, ',', output, 'blu')
				robot.drive(turningSpeed, output)
			print('LANDONNNN')

	robot.drive(-20, 0)
	while(lColor.reflection() < 30 or rColor.reflection() < 30):
		pass
	robot.stop()
	robot.straight(-10)
	#ev3.speaker.beep()
	while True:
		compensator = 2 #Amount to multiply output by
		leftIsBlack = isBlack(lColor)
		rightIsBlack = isBlack(rColor)
		
		diff = lColor.reflection() - rColor.reflection() + cal #finds the difference between the reflections
		if not leftIsBlack and not rightIsBlack:
				doubleWhite(cal)
		#Uncomment for redline (stop and turn around)
		if lColor.reflection() < redA and lColor.reflection() > redB and rColor.reflection() < redA and rColor.reflection() > redB and diff <= 10 and diff >= -10:
			redLine()
		#	pass
		output = -int(multiplier * diff) #gets degrees to turn by

		turningSpeed = math.floor(maxTurnSpeed/(abs(a*diff)+1))

  
		print(turningSpeed, ',', output, 'inverted')
  
		robot.drive(turningSpeed, output)
  
		#robot.drive(driveSpeed, output) #output may need to be limited to within -180, 180 (?)

def leftDetour():
	print('leftdet', detourDone, lColor.reflection())
	#ev3.light(Color.RED)
	#ev3.speaker.beep(1000,400)
	wait(20)
	#ev3.light(Color.GREEN)
	robot.turn(70)

def rightDetour():
	print('rightdet', detourDone, rColor.reflection())
	#ev3.speaker.beep(600,400)
	wait(20)
	robot.turn(-70)

def redLine():
	
	if (lColor.color() == Color.RED or rColor.color() == Color.RED):
		sys.exit()

# Left turn
	elif (lColor.reflection() < rColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
		print('right1')
		robot.turn(-50) #10 small 15 normal
		robot.drive(100, 0)
		while lColor.reflection() < black:
			pass
		robot.stop()
		robot.drive(0, 40)

	# Right turn
	elif (rColor.reflection() < lColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
		robot.turn(50) #10 small 15 normal??
		robot.drive(100, 0)
		while rColor.reflection() < black:
			pass
		robot.stop()
		robot.drive(0, -40)

def doubleBlack(compensator, cal):
	print('doubleblack', compensator)
	robot.stop
	wait(50)
 
	diff = lColor.reflection() - rColor.reflection()

	iteration = 0

 
	while lColor.reflection() < black and rColor.reflection() < black:
		robot.stop()
		robot.straight(7.5)

		if (lColor.color() == Color.RED or rColor.color() == Color.RED):
			redLine()

		#Uncomment for white line
		iteration += 1
		if iteration >= 3:
			checkGreenCol()
			#if iteration >= 10:
			#	robot.drive(10000000, 0)
				#while True:
				#	pass
			whiteLine(cal)

		if diff <= compensator and diff >= -compensator:
			pass


		# Right turn
		elif (lColor.reflection() < rColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
			print('right1')
			robot.turn(12) #10 small 15 normal
			robot.drive(100, 0)
			while lColor.reflection() < black:
				pass
			robot.stop()
			robot.drive(0, 40)

		# Left turn
		elif (rColor.reflection() < lColor.reflection()) and (isBlack(lColor) and isBlack(rColor)):
			robot.turn(-12) #10 small 15 normal??
			robot.drive(100, 0)
			while rColor.reflection() < black:
				pass
			robot.stop()
			robot.drive(0, -40)

		else:
			pass

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
	while lColor.reflection() >= 99 or rColor.reflection() >= 99:
		pass
	robot.stop()

	while lColor.reflection() < 99 or rColor.reflection() < 99:
		if lColor.reflection() < 99 and rColor.reflection() < 99:
			robot.drive(25, 0)
		elif lColor.reflection() < 99:
			robot.drive(0, 25)
		else:
			robot.drive(0,-25)



def rescue():
	global rescueCount
	robot.stop()
	claw.run_angle(-200, 50)

	centerRescue()

	startAngle = robot.angle()
 
	maxCanDist = 250
	blockDist = 270
 
	wait(20)
	robot.straight(220)
	wait(20)
	robot.turn(-30)
	#print(ultraS.distance())
	#if ultraS.distance() < maxCanDist+50:
	#	robot.drive(0,-50)
	#	while ultraS.distance() < maxCanDist+50:
	#		pass
	#	robot.stop()
	#else:
	#	robot.turn(-30)
	#	print("couldn't find block")
	#print(ultraS.distance())
	wait(10)
	
 
 
	#robot.drive(0, -30)
 
	while (startAngle - robot.angle()) < 360:
		robot.drive(0, -40)
		if ultraS.distance() < maxCanDist:
			canDist = ultraS.distance()
			robot.stop()
			wait(50)

			blockMax = 300
			blockMin = 200
			#check if orange
			#while canDist < blockMax and canDist > blockMin and (robot.angle() - startAngle) < 130 and (robot.angle() - startAngle) > 170:
			#	robot.drive(0,20)#change
			#robot.stop()
			#wait(10)

			#finds center of can
			robot.turn(-20)

			robot.drive(0,-15)#small turn
			while ultraS.distance() < maxCanDist:
				pass
			robot.stop()
			canRight = robot.angle()
			#ev3.speaker.beep()
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
			#ev3.speaker.beep()
			#calc center here
			canCompensation = canRight - canLeft
			print(canRight,canLeft,canCompensation,canDist)
			robot.turn(canCompensation/2)
			
			robot.straight(canDist - 100)
			#ev3.speaker.beep()
			robot.stop()
			wait(20)

			if frontColor.color() == Color.RED: # or frontColor.reflection == 0:
				robot.straight(-(canDist - 30))
				robot.turn(-40)#change this if going forward again
				robot.drive(0, -50)
			else:
				lifter.run_angle(100,90,wait=True)
				wait(20)
				robot.straight(45)
				
				#claw.run_time(100,1000,wait=True) #centers it with claw
				#claw.run_angle(-20,50,wait=True) #reopens claw
#				claw.stop()
				#robot.straight(-24)
				#lifter.run_angle(-100,90,wait=True)
				#robot.straight(50) #forward to check colour
#				if frontColor.reflection() < 10:
#					robot.straight(-canDist+25)
#					robot.turn(-40)#change this if going forward again
#					robot.drive(0, -20)
#				else:
				#robot.straight(-40)
				#robot.straight(10)
				#lifter.run_angle(95,90,wait=True)
				#robot.straight(8) #might knock can over
				claw.run(100) #grabs can
				wait(500)
				#robot.straight(-12)
				#wait(20)
				lifter.run_angle(95,-90,wait=True) #lifts can
				#robot.straight(14)
				robot.straight(-(canDist-55)) #back to middle
				robot.turn((startAngle-robot.angle())) #face block
				if funnyBlok == 1:
					if ultraS.distance() <= blockMax:
						blockPos = 0
					else:
						robot.turn(90)
						if ultraS.distance() <= blockMax:
							blockPos = 90
						else:
							robot.turn(-180)
							if ultraS.distance() <= blockMax:
								blockPos = -90
							else:
								pass #sys.exit()
				else:
					pass


					robot.straight(blockDist-21) #goto block
					
	#				if frontColor.color() != Color.RED:
	#					while frontColor.color() != Color.RED:
	#						robot.drive(0,-20)
	#					robot.stop()

					lifter.run_angle(30,20) #lower lifter
					wait(250)
					claw.stop()
					claw.run_angle(-100,50,wait=True) #drop can
					lifter.run_angle(30,-20)
					robot.straight(-blockDist+21)
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
	# robot.straight(-50)
	# wait(20)
	# robot.turn(180)
	if (lColor.color() == Color.RED or rColor.color() == Color.RED):
		ev3.speaker.say("finally the suffering is over")
		sys.exit()

#Handles all movement
def move(cal):
	global detourDone
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
		
		if lColor.reflection() < redA and lColor.reflection() > redB and rColor.reflection() < redA and rColor.reflection() > redB and diff <= 10 and diff >= -10:
			redLine()
		if leftIsBlack and rightIsBlack:
				doubleBlack(compensator, cal)
		#Uncomment for redline
		
		#	pass
		output = int(multiplier * diff) #gets degrees to turn by

		
		
		#robot.drive(driveSpeed, output) #output may need to be limited to within -180, 180 (?)

		turningSpeed = math.floor(maxTurnSpeed/(abs(a*diff)+1))
  
		print(turningSpeed, ',', output, 'normal')
		robot.drive(turningSpeed, output)
		# if detourDone <= 1:
		# 	if lColor.reflection() < redA and lColor.reflection() > redB:
		# 		robot.stop()
		# 		wait(20)
		# 		if lColor.color() == Color.RED:
		# 			leftDetour()
		# 			detourDone = detourDone + 1

		# 	if rColor.reflection() < redA and rColor.reflection() > redB:
		# 		robot.stop()
		# 		wait(20)
		# 		if rColor.color() == Color.RED:
		# 			rightDetour()
		# 			detourDone = detourDone + 1
					#NARROW DOWN RANGE!!!!!!!!



def startMessage():
	ev3.speaker.set_speech_options(voice="m7")
	ev3.speaker.set_volume(10000)
	#Arguments should be 1 and the number of possible outcomes
	rand = random.randint(0, len(helloMessages) - 1)
	ev3.speaker.say(helloMessages[rand])

def cal():
	dif = lColor.reflection() - rColor.reflection()
	return dif

def initiate():
	#startMessage()
	lifter.run_angle(100,-90, wait=False)
	claw.run_until_stalled(100)
	#ev3.speaker.say("Close the claw you nons")
	#ev3.speaker.beep()
	while len(ev3.buttons.pressed()) == 0:
		pass
	dif = cal()
	print(dif)
	wait(200)
	#ev3.speaker.beep()
	while len(ev3.buttons.pressed()) == 0:
		pass

	#ev3.speaker.beep(200,20)

	move(dif)

def landon():
	ev3.speaker.set_speech_options(voice="m7")
	ev3.speaker.set_volume(100)

	bees = """
	According to all known laws
of aviation,
there is no way a bee
should be able to fly.
Its wings are too small to get
its fat little body off the ground.
The bee, of course, flies anyway
because bees don't care
what humans think is impossible.
Yellow, black. Yellow, black.
Yellow, black. Yellow, black.
Ooh, black and yellow!
Let's shake it up a little.
Barry! Breakfast is ready!
Ooming!
Hang on a second.
Hello?
- Barry?
- Adam?
- Oan you believe this is happening?
- I can't. I'll pick you up.
Looking sharp.
Use the stairs. Your father
paid good money for those.
Sorry. I'm excited.
Here's the graduate.
We're very proud of you, son.
A perfect report card, all B's.
Very proud.
Ma! I got a thing going here.
- You got lint on your fuzz.
- Ow! That's me!
- Wave to us! We'll be in row 118,000.
- Bye!
Barry, I told you,
stop flying in the house!
- Hey, Adam.
- Hey, Barry.
- Is that fuzz gel?
- A little. Special day, graduation.
Never thought I'd make it.
Three days grade school,
three days high school.
Those were awkward.
Three days college. I'm glad I took
a day and hitchhiked around the hive.
You did come back different.
- Hi, Barry.
- Artie, growing a mustache? Looks good.
- Hear about Frankie?
- Yeah.
- You going to the funeral?
- No, I'm not going.
Everybody knows,
sting someone, you die.
Don't waste it on a squirrel.
Such a hothead.
I guess he could have
just gotten out of the way.
I love this incorporating
an amusement park into our day.
That's why we don't need vacations.
Boy, quite a bit of pomp...
under the circumstances.
- Well, Adam, today we are men.
- We are!
- Bee-men.
- Amen!
Hallelujah!
Students, faculty, distinguished bees,
please welcome Dean Buzzwell.
Welcome, New Hive Oity
graduating class of...
...9:15.
That concludes our ceremonies.
And begins your career
at Honex Industries!
Will we pick ourjob today?
I heard it's just orientation.
Heads up! Here we go.
Keep your hands and antennas
inside the tram at all times.
- Wonder what it'll be like?
- A little scary.
Welcome to Honex,
a division of Honesco
and a part of the Hexagon Group.
This is it!
Wow.
Wow.
We know that you, as a bee,
have worked your whole life
to get to the point where you
can work for your whole life.
Honey begins when our valiant Pollen
Jocks bring the nectar to the hive.
Our top-secret formula
is automatically color-corrected,
scent-adjusted and bubble-contoured
into this soothing sweet syrup
with its distinctive
golden glow you know as...
Honey!
- That girl was hot.
- She's my cousin!
- She is?
- Yes, we're all cousins.
- Right. You're right.
- At Honex, we constantly strive
to improve every aspect
of bee existence.
These bees are stress-testing
a new helmet technology.
- What do you think he makes?
- Not enough.
Here we have our latest advancement,
the Krelman.
- What does that do?
- Oatches that little strand of honey
that hangs after you pour it.
Saves us millions.
Oan anyone work on the Krelman?
Of course. Most bee jobs are
small ones. But bees know
that every small job,
if it's done well, means a lot.
But choose carefully
because you'll stay in the job
you pick for the rest of your life.
The same job the rest of your life?
I didn't know that.
What's the difference?
You'll be happy to know that bees,
as a species, haven't had one day off
in 27 million years.
So you'll just work us to death?
We'll sure try.
Wow! That blew my mind!
"What's the difference?"
How can you say that?
One job forever?
That's an insane choice to have to make.
I'm relieved. Now we only have
to make one decision in life.
But, Adam, how could they
never have told us that?
Why would you question anything?
YOUR MOTHER IS RATHER SUSPISIOUSOISUS BUT YOUR ARE ACTUALLY GAY LMAO ANDREW DHARMA THE FARMER
We're bees.
"""
	#ev3.speaker.say(bees)
	#while True:
	#	ev3.speaker.beep(lColor.reflection()*6, random.randint(0, 50))
	#ev3.speaker.play_file('necron.mp3')

def test():
	#initiate()
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

##funnythread = threading.Thread(target=landon)

#test()
#funnythread.start()
initiate()
#landon()