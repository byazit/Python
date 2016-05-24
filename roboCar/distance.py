
# Import required Python libraries
import time
import RPi.GPIO as GPIO
import numpy as np
import sys

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)

# Define GPIO to use on Pi
GPIO_TRIGGER = 16
GPIO_ECHO = 18
GPIO_LED=12
GPIO_SERVO=11

# back motor control
BACK_A1=8
BACK_A2=10
GPIO.setup(BACK_A1, GPIO.OUT)
GPIO.setup(BACK_A2, GPIO.OUT)

#front motor
FRONT_B1=13
FRONT_B2=15
GPIO.setup(FRONT_B1, GPIO.OUT)
GPIO.setup(FRONT_B2, GPIO.OUT)

speed=50
clock=1
p=GPIO.PWM(BACK_A1,clock)
q=GPIO.PWM(BACK_A2,clock)

p.start(0)
q.start(0)

print "Ultrasonic Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
GPIO.setup(GPIO_LED, GPIO.OUT)     #led
GPIO.setup(GPIO_SERVO, GPIO.OUT)	 #servo
sonicPulse=GPIO.PWM(GPIO_SERVO,50)
sonicPulse.start(7.5)
# Set trigger to False (Low)
myList=[]
maxV=[]
pp=0
chk=0

def chkAll():
  GPIO.output(GPIO_TRIGGER, False)
  # Allow module to settle
  time.sleep(0.5)
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()
    #print "Echo start"
  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()
    #print "echo stop"
  # Calculate pulse length
  elapsed = stop-start

  # Distance pulse travelled in that time is time
  # multiplied by the speed of sound (cm/s)
  distance = elapsed * 34000
  distance = distance / 2
  return myList.append(distance)

def sonic():
  global chk
  GPIO.output(GPIO_TRIGGER, False)
  # Allow module to settle
  time.sleep(0.5)
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()
    #print "Echo start"
  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()
    #print "echo stop"
  # Calculate pulse length
  elapsed = stop-start

  # Distance pulse travelled in that time is time
  # multiplied by the speed of sound (cm/s)
  distance = elapsed * 34000
  distance = distance / 2
  print "-------------> "
  if chk ==0 :
    rules(distance)
  else:
    return myList.append(distance)
#led blinking
def blink(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(1)  
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(1)  
        return

#Rules for when to stop and make dicition
def rules(distance):
  print "Distance : %.1f" % distance
  if distance<70:
    print "Object detected : %.1f" % distance
    global pp
    pp=1
    p.ChangeDutyCycle(0)
    #sys.exit()
    #checking()
  else:
    mForward()
    
    
  return

#which way to go
def motorDrive(myList):
  global pp
  #front movement
#  back= max(myList)
#  if back>70:
  if back==myList[0]:
    #print "max--0 value is: %.1f" % myList[0]
    if myList[0] >70:
      print "I can go forward"
      straight()
      mForward()
      pp=0
    else:
      straight()
      mBack()
      time.sleep(1)
    #rules( myList[0])
  #right movement
  elif back==myList[1]:
    #print "max--1 value is: %.1f" % myList[1]
    if myList[1] >70:
      mRight()
      mForward()
      pp=1
    else:
      mLeft()
      mBack()
      time.sleep(1)
    #rules( myList[1])
  #left movement
  elif back==myList[2]:
    #print "max--2 value is: %.1f" % myList[2]
    if myList[1] >70:
      mLeft()
      mForward()        
      pp=1
    else:
      mRight()
      mBack()
      time.sleep(1)
#  else:
#    mBack()
    #rules( myList[2])
  #back movement

#checking for objects
def checking():
    global chk
    chk=1
    sonicPulse.ChangeDutyCycle(7.5)
    print "Checking front"
#    time.sleep(1)
    sonic()

    sonicPulse.ChangeDutyCycle(12.5)
    print "checking right"
#    time.sleep(1)
    sonic()
 
    sonicPulse.ChangeDutyCycle(2.5)
    print "checking left"
#    time.sleep(1)
    sonic()

    sonicPulse.ChangeDutyCycle(7.5)
    motorDrive(myList)
    del myList[:]
    back=0
    chk=0
#moto forward
def mForward():
    for i in range(speed):
      p.ChangeDutyCycle(i)
#moto back

def mBack():
  print "back"
  p.ChangeDutyCycle(0)
  for i in range(100):
    q.ChangeDutyCycle(i)
  time.sleep(1)
  q.ChangeDutyCycle(0)

#motor right
def mRight():
  GPIO.output(FRONT_B1,1)
  GPIO.output(FRONT_B2,0)
#motor left
def mLeft():
  GPIO.output(FRONT_B1,0)
  GPIO.output(FRONT_B2,1)
#motor straight
def straight():
  GPIO.output(FRONT_B1,0)
  GPIO.output(FRONT_B2,0)

while True:
  try:   
    if(pp==0):
      sonic()
      straight()
      time.sleep(0.5)
    else:
      checking()

    """
    # That was the distance there and back so halve the value
    blink(GPIO_LED)
    # Reset GPIO settings      
    sonicPulse.ChangeDutyCycle(7.5)
    print "Checking front"
    time.sleep(1)
    sonic()
    time.sleep(1)
    sonicPulse.ChangeDutyCycle(12.5)
    print "checking right"
    time.sleep(1)
    sonic()
    time.sleep(1)
    sonicPulse.ChangeDutyCycle(4.5)
    print "checking left"
    time.sleep(1)
    sonic()
    time.sleep(1)
    sonicPulse.ChangeDutyCycle(7.5)

    motorDrive(myList)
    maxVal=max(myList) 
    print "Max function-- : %.1f" % maxVal
    maxVal=0
    del myList[:]
    #motorDrive(maxVal)
    """
  except KeyboardInterrupt:
    print "Program ended by user.\n"
    p.ChangeDutyCycle(0)
    GPIO.cleanup()
    break 
      
print 'Success!'
