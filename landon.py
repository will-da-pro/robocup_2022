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


#objects
ev3 = EV3Brick()
e = 1

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

#program

def startMessage():
	ev3.speaker.set_speech_options(voice="m2")
	ev3.speaker.set_volume(10000)
	#Arguments should be 1 and the number of possible outcomes
	#rand = random.randint(0, len(helloMessages) - 1)
	#ev3.speaker.say(helloMessages[rand])

def initiate(e):
	robot.straight(-5)
	lifter.run_angle(100, -40, wait=True)
	#startMessage()
	while True:
		e = random.randint(-20, 20)
		robot.drive(e*10, e)
		wait(50)

def landon():
	ev3.speaker.set_speech_options(voice="f2")
	ev3.speaker.set_volume(10000)

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
YOUR MOTHER IS RATHER SUSPISIOUSOISUS BUT YOUR ARE ACTUALLY lanfob LMAO ANDREW DHARMA THE FARMER
We're bees.
"""
	ev3.speaker.say(bees)
	while True:
		ev3.speaker.beep(lColor.reflection()*6, random.randint(0, 50))
	#ev3.speaker.play_file('necron.mp3')


funnythread = threading.Thread(target=landon)

funnythread.start()
initiate(e)
#landon()