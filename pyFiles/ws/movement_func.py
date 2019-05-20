import wiringpi
import time
import sys

'''SETUP wiringPi for Modification'''
wiringpi.wiringPiSetup()
wiringpi.pinMode(0,1)
wiringpi.pinMode(1,1)
wiringpi.pinMode(2,1)
wiringpi.pinMode(3,1)

wiringpi.pinMode(4,1) #output
wiringpi.pinMode(5,0) #input
masterOff_s = False

#0 = STOP | 1 = GO | 2 = PAUSE
autoFile = open("masterOff.txt","w")
file2 = open("masterOff.txt","w")
file2.write("0")
file2.close()

def movDie():
	file2 = open("masterOff.txt","w")
	file2.write("0")
	file2.close()
	sys.exit()
	return
	
def turnOffPins():
	#print("WPI: STOPPING ALL PINS")
	wiringpi.digitalWrite(0,0);
	wiringpi.digitalWrite(1,0);
	wiringpi.digitalWrite(2,0);
	wiringpi.digitalWrite(3,0);
	return

def moveForward():
	turnOffPins()
	if(readmasterOff()==False):
		print("WPI: Moving Forward")
		wiringpi.digitalWrite(0, 1)
		readmasterOff()
		wiringpi.digitalWrite(2, 1)
		readmasterOff()
	return

def moveBackward():
	turnOffPins()
	if(readmasterOff()==False):
		print("WPI: Moving Backward")
		wiringpi.digitalWrite(1, 1)
		readmasterOff()
		wiringpi.digitalWrite(3, 1)
		readmasterOff()
	return

def rotateRight():
	turnOffPins()
	if(readmasterOff()==False):
		print("WPI: Rotating Right")
		wiringpi.digitalWrite(0, 1)
		readmasterOff()
		wiringpi.digitalWrite(3, 1)
		readmasterOff()
	return

def rotateLeft():
	turnOffPins()
	if(readmasterOff()==False):
		print("WPI: Rotating Left")
		wiringpi.digitalWrite(1, 1)
		readmasterOff()
		wiringpi.digitalWrite(2, 1)
		readmasterOff()
	return
	
def readmasterOff():
	file = open("masterOff.txt","r")
	line = list(file.readlines())
	line=line[0].splitlines()[0]
	if(line=="0"):
		print("Master says to turn off.")
		turnOffPins()
		movDie()
		return True
	else:
		return False
	
def readRoboAutoStop():
	file = open("masterOff.txt","r")
	line = list(file.readlines())
	line=line[0].splitlines()[0]
	if(line=="true"):
		print("yeah")
		turnOffPins()
		movDie()
		return True
	else:
		return False

def AutoPinGo():
	wiringpi.digitalWrite(4,1)
	return

def ResponsePinStop():
	if wiringpi.digitalRead(5)==1:
		wiringpi.digitalWrite(4,0)
		return True
	else:
		return False
		
def AutoPinStop():
	wiringpi.digitalWrite(4,0)
	return


def movement_func(arg1):
	moveforwardtime = 0.8
	moveside = 0.4
	arg1 = int(arg1)
	if arg1==12345:
		autoFile = open("masterOff.txt","w")
		autoFile.write('0')
		autoFile.close()
		time.sleep(2)
		autoFile = open("masterOff.txt","w")
		autoFile.write('1')
		autoFile.close()
		
	else:
		readRoboAutoStop()
		
		if arg1==1:
			#forward
			moveForward()
		elif arg1==2:
			#left
			#moveForward()
			#time.sleep(moveforwardtime)
			rotateLeft()
			time.sleep(moveside)
			turnOffPins()
		elif arg1==3:
			#right
			rotateRight()
			time.sleep(moveside)
			turnOffPins()
		elif arg1==4:
			#reverse
			moveBackward()
		elif arg1==5:
			#stop
			turnOffPins()
		elif arg1==6:
			#rotateLeft
			rotateLeft()
		elif arg1==7:
			#rotateRight
			rotateRight()
		elif arg1==8:
			#360CounterClockwise
			print("WPI: 360: CounterClockwise")
			rotateLeft()
			time.sleep(0.8)
			turnOffPins()
		elif arg1==9:
			#360Clockwise
			print("WPI: 360: Clockwise")
			moveForward()
			time.sleep(0.6)
			rotateRight()
			time.sleep(1.2)
			turnOffPins()
		elif arg1==12345:
			autoFile = open("masterOff.txt","w")
			autoFile.write('0')
			autoFile.close()
			time.sleep(2)
			autoFile = open("masterOff.txt","w")
			autoFile.write('1')
			autoFile.close()
		else:
			turnOffPins()
		
	return

if __name__ == "__main__":
    movement_func(sys.argv[1])
