# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import datetime

from rpi_ws281x import *

# LED strip configuration:
LED_1_COUNT      = 600      # Number of LED pixels.
LED_1_PIN        = 18      # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_1_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA        = 10      # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_1_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL    = 0       # 0 or 1
LED_1_STRIP      = ws.WS2811_STRIP_GRB


LED_2_COUNT      = 600      # Number of LED pixels.
LED_2_PIN        = 13      # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_2_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_2_DMA        = 11      # DMA channel to use for generating signal (Between 1 and 14)
LED_2_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_2_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_2_CHANNEL    = 1       # 0 or 1
LED_2_STRIP      = ws.WS2811_STRIP_GRB

count_i = 0

def multiColorWipe(color1, color2, wait_ms=5):
	global strip1
	global strip2
	"""Wipe color across multiple LED strips a pixel at a time."""
	global count_i
	for i in range(strip1.numPixels()):
		strip1.setPixelColor(i, color1)
		strip2.setPixelColor(i, color2)
	
	#for i in range(strip1.numPixels()):
		#if i % 2 == 0:
			# even number
			#strip1.setPixelColor(i, color1)
			#strip1.show()
			#time.sleep(wait_ms/1000.0)
			#strip2.setPixelColor(i, color2)
			#strip2.show()
			#time.sleep(wait_ms/1000.0)
			#print("even number:"+str(i))
		#else:
			# odd number
			#strip1.setPixelColor(i, color2)
			#strip1.show()
			#time.sleep(wait_ms/1000.0)
			#strip2.setPixelColor(i, color1)
			#strip2.show()
			#time.sleep(wait_ms/1000.0)
			#print("odd number:"+str(i))
	strip1.show()
	time.sleep(0.02)
	strip2.show()
	time.sleep(0.02)
	count_i = count_i + 1

	#time.sleep(1)

def blackout(strip):
	for i in range(max(strip1.numPixels(), strip1.numPixels())):
		strip.setPixelColor(i, Color(0,0,0))
		strip.show()

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel objects with appropriate configuration for each strip.
	strip1 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS, LED_1_CHANNEL, LED_1_STRIP)
	strip2 = Adafruit_NeoPixel(LED_2_COUNT, LED_2_PIN, LED_2_FREQ_HZ, LED_2_DMA, LED_2_INVERT, LED_2_BRIGHTNESS, LED_2_CHANNEL, LED_2_STRIP)


	# Intialize the library (must be called once before other functions).
	strip1.begin()
	strip2.begin()

	print ('Press Ctrl-C to quit.')

	# Black out any LEDs that may be still on for the last run
	#blackout(strip1)
	#blackout(strip2)
	print("Start:")
	print(datetime.datetime.now())
	while True:
		global count_i
		if count_i > 100:
			print("stop:")
			print(datetime.datetime.now())
			break
		# Multi Color wipe animations.
		multiColorWipe(Color(255, 0, 0), Color(0, 255, 0))  # Red wipe
		multiColorWipe(Color(0, 255, 0), Color(0, 0, 255))  # Blue wipe
		multiColorWipe(Color(0, 0, 255), Color(255, 0, 0))  # Green wipe
		multiColorWipe(Color(255, 255, 255), Color(255, 255, 255))  # Composite White wipe
