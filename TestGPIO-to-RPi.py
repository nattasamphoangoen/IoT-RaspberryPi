import RPi.GPIO as GPIO #Add GPIO library to a Python sketch
import time #Add time library to a Python sketch

GPIO.setmode(GPIO.BOARD) #Setup GPIO using Board numbering
GPIO.setup(11, GPIO.OUT) #Setup pin 11 to output
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
status = 0
while True:
	if (status==0): 
		GPIO.output(11,GPIO.HIGH) 
		print("Input = 1, HIGH")
	else:
		GPIO.output(11,GPIO.LOW) 
		print("Input = 0, LOW") 
	time.sleep(0.5) 
	if(GPIO.input(12)==1): 
		time.sleep(0.1) 
		while(GPIO.input(12)==1): 
			time.sleep(0.1)
		status = ~status