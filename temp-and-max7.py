import sys
import time
import Adafruit_DHT
import RPi.GPIO as GPIO

sensor = Adafruit_DHT.DHT11
pin = 4

GPIO.setmode(GPIO.BOARD)

LATCH = 24 # CS
CLK = 23 # Clock
dataBit = 19 # DIN

GPIO.setup(LATCH, GPIO.OUT) 
GPIO.setup(CLK, GPIO.OUT) 
GPIO.setup(dataBit, GPIO.OUT)

# Setup IO
GPIO.output(LATCH, 0)
GPIO.output(CLK, 0)

def pulseCLK():
	GPIO.output(CLK, 1)
	time.sleep(.001) 
	GPIO.output(CLK, 0)
	return

def pulseCS():
	GPIO.output(LATCH, 1)
	time.sleep(.001)
	GPIO.output(LATCH, 0)
	return

# shift byte into MAX7219
# MSB out first!
def ssrOut(value):
	for x in range(0,8):
		temp = value & 0x80
		if temp == 0x80:
			GPIO.output(dataBit, 1) # data bit HIGH
		else:
			GPIO.output(dataBit, 0) # data bit LOW
		pulseCLK()
		value = value << 0x01 # shift left 
	return

# initialize MAX7219 4 digits BCD
def initMAX7219():

	# set decode mode
	ssrOut(0x09) # address
	ssrOut(0x00); # no decode data
	# ssrOut(0xFF) # 4-bit BCD decode eight digits
	pulseCS();

	# set intensity
	ssrOut(0x0A) # address
	ssrOut(0x04) # 9/32s
	pulseCS()

	# set scan limit 0-7
	ssrOut(0x0B); # address
	ssrOut(0x07) # 8 digits
	# ssrOut(0x03) # 4 digits
	pulseCS()

	# set for normal operation
	ssrOut(0x0C) # address
	# ssrOut(0x00); // Off
	ssrOut(0x01) # On
	pulseCS()
	# clear to all 0s.
	for x in range(0,9):
		ssrOut(x)
		ssrOut(0x0f)
		pulseCS()
	return

def writeMAX7219(digit, location, data):
	ssrOut(location)
	ssrOut(data | (digit<<7))
	pulseCS()
	return
def displayOff():
	# set for normal operation
	ssrOut(0x0C) # address
	ssrOut(0x00); # Off
	# ssrOut(0x01) # On
	pulseCS()
	return

def displayOn():
	# set for normal operation
	ssrOut(0x0C) # address
	# ssrOut(0x00); # Off
	ssrOut(0x01) # On
	pulseCS()
	return

Encode7Seg = [ 0b1111110,0b0110000,0b1101101,0b1111001,
		0b0110011,0b1011011,0b1011111,0b1110000,
		0b1111111,0b1111011,0b1110111,0b0011111,
		0b1001110,0b0111101,0b1001111,0b1000111 ]

time.sleep(1) 
initMAX7219()

while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		print 'Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity)

		TemppX = (int)(temperature * 10)
		Tempp0 = TemppX % 10
		TemppX = TemppX / 10
		Tempp1 = TemppX % 10
		TemppX = TemppX / 10
		Tempp2 = TemppX % 10

		HumidX = (int)(humidity * 10)
		Humid0 = HumidX % 10
		HumidX = HumidX / 10
		Humid1 = HumidX % 10
		HumidX = HumidX / 10
		Humid2 = HumidX % 10

		writeMAX7219( 0, 8, Encode7Seg[Tempp2])
		writeMAX7219( 1, 7, Encode7Seg[Tempp1])
		writeMAX7219( 0, 6, Encode7Seg[Tempp0])
		writeMAX7219( 0, 5, 0b00001101) #Code=tabcdefgh
		writeMAX7219( 0, 4, Encode7Seg[Humid2])
		writeMAX7219( 1, 3, Encode7Seg[Humid1])
		writeMAX7219( 0, 2, Encode7Seg[Humid0])
		writeMAX7219( 0, 1, 0b00010111) #Code=tabcdefgh
		time.sleep(2)
	else:
		print 'Failed to get reading. Try again!'