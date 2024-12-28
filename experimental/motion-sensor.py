#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# GPIO pins for the ultrasonic sensor
TRIG = 11  # Trigger pin - sends the ultrasonic pulse
ECHO = 12  # Echo pin - receives the reflected pulse

def setup():
	# Set up GPIO mode and configure pins
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(TRIG, GPIO.OUT)  # Trigger pin as output
	GPIO.setup(ECHO, GPIO.IN)   # Echo pin as input

def distance():
	# Ensure trigger pin is low
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	# Send a 10-microsecond pulse to trigger the sensor
	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	# Wait for the echo pin to go high (pulse sent)
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	# Wait for the echo pin to go low (pulse received back)
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	# Calculate distance using the time difference
	# Speed of sound = 340 m/s
	# Divide by 2 because the pulse travels to and from the object
	# Multiply by 100 to convert to centimeters
	during = time2 - time1
	return during * 340 / 2 * 100

def loop():
	# Continuously measure and print the distance
	while True:
		dis = distance()
		print (dis, 'cm')
		print ('')
		time.sleep(0.3)  # Wait 300ms between measurements

def destroy():
	# Clean up GPIO pins when program exits
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		# Handle when user presses Ctrl+C
		destroy()
