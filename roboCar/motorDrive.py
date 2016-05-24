import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

"""back motor"""
BACK_A1=8
BACK_A2=10
GPIO.setup(BACK_A1, GPIO.OUT)
GPIO.setup(BACK_A2, GPIO.OUT)
"""front motor"""
FRONT_B1=13
FRONT_B2=15
GPIO.setup(FRONT_B1, GPIO.OUT)
GPIO.setup(FRONT_B2, GPIO.OUT)
""" 
GPIO.output(11,1)
GPIO.output(12,0)
time.sleep(0.5)
GPIO.output(11,0)
GPIO.output(12,1)
time.sleep(0.5)
"""
speed=100
clock=20
p=GPIO.PWM(BACK_A1,clock)
q=GPIO.PWM(BACK_A2,clock)

p.start(0)
q.start(0)
"""
GPIO.output(FRONT_B1,1)
GPIO.output(FRONT_B2,0)
time.sleep(0.5)
GPIO.output(FRONT_B1,0)
GPIO.output(FRONT_B2,1)
time.sleep(0.5)
"""
try:

	while True:
					for i in range(speed):
								p.ChangeDutyCycle(i)
								time.sleep(0.02)
					for i in range(speed):
								p.ChangeDutyCycle(speed-i)

					p.ChangeDutyCycle(0)

					for i in range(speed):
								q.ChangeDutyCycle(i)
								time.sleep(0.02)
					for i in range(speed):
								q.ChangeDutyCycle(speed-i)

					q.ChangeDutyCycle(0)
except KeyboardInterrupt:
				pass
p.stop()
q.stop()
"""
GPIO.output(8,1)
GPIO.output(10,0)
time.sleep(0.5)
GPIO.output(8,0)
GPIO.output(10,1)
time.sleep(0.5)
"""
GPIO.cleanup()


