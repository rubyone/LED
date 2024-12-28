#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import sys
import os

# Add the parent directory to Python path if LED1.py is in the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, "/home/pi/.local/lib/python3.9/site-packages/")
from rpi_ws281x import *
from LED1 import LEDController

# GPIO pins for the ultrasonic senso
# TRIG = 11  # Trigger pin - sends the ultrasonic pulse
# ECHO = 12  # Echo pin - receives the reflected pulse

TRIG = 23  # GPIO23 (Pin 16)
ECHO = 24  # GPIO24 (Pin 18)

# Motion detection parameters
THRESHOLD = 5.0  # Distance change threshold in cm to detect motion
SAMPLE_INTERVAL = 0.1  # Time between measurements in seconds
SAMPLES_TO_STABLE = 3  # Number of stable readings needed to confirm no motion
TIMEOUT_MINUTES = 5  # Time without motion before turning off LEDs

class MotionSensorLED:
	def __init__(self):
		self.led_controller = LEDController()
		self.setup()
		self.last_motion_time = time.time()
		self.leds_on = False

	def setup(self):
		# Set up GPIO mode and configure pins
        # GPIO.setmode(GPIO.BOARD) # not working in the configuration
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(TRIG, GPIO.OUT)  # Trigger pin as output
		GPIO.setup(ECHO, GPIO.IN)   # Echo pin as input

	def distance(self):
		# Ensure trigger pin is low
		GPIO.output(TRIG, 0)
		time.sleep(0.000002)

		# Send a 10-microsecond pulse to trigger the sensor
		GPIO.output(TRIG, 1)
		time.sleep(0.00001)
		GPIO.output(TRIG, 0)

		# Wait for the echo pin to go high (pulse sent)
		pulse_start = time.time()
		timeout = pulse_start + 0.1  # 100ms timeout
		while GPIO.input(ECHO) == 0:
			if time.time() > timeout:
				return None
			pulse_start = time.time()

		# Wait for the echo pin to go low (pulse received back)
		pulse_end = time.time()
		timeout = pulse_end + 0.1  # 100ms timeout
		while GPIO.input(ECHO) == 1:
			if time.time() > timeout:
				return None
			pulse_end = time.time()

		# Calculate distance using the time difference
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 34000 / 2  # Speed of sound = 340 m/s
		return round(distance, 2)

	def turn_on_leds(self):
		if not self.leds_on:
			print("Turning LEDs on")
			# Start rainbow animation
			self.led_controller.start_animation(self.led_controller.rainbow)
			self.leds_on = True

	def turn_off_leds(self):
		if self.leds_on:
			print("Turning LEDs off")
			self.led_controller.stop_animation = True
			self.led_controller.reset()
			self.leds_on = False

	def detect_motion(self):
		previous_distance = None
		stable_count = 0
		motion_detected = False

		print("Motion sensor active. Press Ctrl+C to exit.")

		while True:
			current_distance = self.distance()
			current_time = time.time()
			
			# Skip invalid readings
			if current_distance is None:
				continue

			# First reading
			if previous_distance is None:
				previous_distance = current_distance
				continue

			# Calculate change in distance
			distance_change = abs(current_distance - previous_distance)

			# Check for motion
			if distance_change > THRESHOLD:
				if not motion_detected:
					print(f"Motion detected! Distance changed by {round(distance_change, 2)} cm")
					print(f"Previous: {previous_distance} cm, Current: {current_distance} cm")
					motion_detected = True
					self.last_motion_time = current_time
					self.turn_on_leds()
				stable_count = 0
			else:
				stable_count += 1
				if stable_count >= SAMPLES_TO_STABLE and motion_detected:
					print("Motion stopped")
					motion_detected = False

			# Check if we should turn off LEDs due to inactivity
			if current_time - self.last_motion_time > (TIMEOUT_MINUTES * 60):
				self.turn_off_leds()

			previous_distance = current_distance
			time.sleep(SAMPLE_INTERVAL)

	def destroy(self):
		# Clean up GPIO pins and turn off LEDs when program exits
		self.turn_off_leds()
		GPIO.cleanup()

def main():
	motion_sensor = MotionSensorLED()
	try:
		motion_sensor.detect_motion()
	except KeyboardInterrupt:
		print("\nExiting...")
		motion_sensor.destroy()

if __name__ == "__main__":
	main()
