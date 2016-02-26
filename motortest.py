#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
 
MotorPin1   = 18    
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)          # Numbers GPIOs by physical location
GPIO.setup(MotorPin1, GPIO.OUT)   # mode --- output
GPIO.output(MotorPin1, GPIO.HIGH)
time.sleep(5)
GPIO.output(MotorPin1, GPIO.LOW)


