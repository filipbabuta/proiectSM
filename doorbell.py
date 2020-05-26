# Copyright (c) 2014 Adafruit Industries Author: Tony DiCola
# Display Library : Adafruit SDD1306 Python
#Credits: www.plusivo.com
#Lesson 6: Ultrasonic HC-SR04+

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import time
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import smtplib
from datetime import datetime

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

trig = 24
echo = 25
buzzer=8

#set the trigger pin as OUTPUT and the echo as INPUT and buzzer as OUTPUT
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

while 1: 
    
    	disp.clear()
    	#set the trigger to HIGH
	GPIO.output(trig, GPIO.HIGH)
	#sleep 0.00001 s and the set the trigger to LOW
	time.sleep(0.00001)
	GPIO.output(trig, GPIO.LOW)
	#save the start and stop times
	start = time.time()
	stop = time.time()
	#modify the start time to be the last time until
	#the echo becomes HIGH
	while GPIO.input(echo) == 0:
		start = time.time()
	#modify the stop time to be the last time until
	#the echo becomes LOW
	while  GPIO.input(echo) == 1:
		stop = time.time()

	#get the duration of the echo pin as HIGH
	duration = stop - start
	#calculate the distance
	distance = 34300/2 * duration
    	if distance < 30:
		smtpUser='test.gyro.sm@gmail.com'
  		smtpPass='testac123'
		toAdd='test.gyro.sm@gmail.com'
  		fromAdd=smtpUser
		now = datetime.now()
  		dt_string = now.strftime("%d-%b-%Y (%H:%M:%S)")
  		#print dt_string
		msg="The DoorBell has ringed at "
		subject= msg + dt_string
		header='To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
		body= ' From within a Python script'
		#print header + '\n' + body
		server=smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(smtpUser,smtpPass)
  		server.sendmail(fromAdd,toAdd, header + '\n' + body)
  		server.quit()
      		for i in range(1,3):
        		disp.clear()
        		GPIO.output(buzzer,GPIO.HIGH)
        		img=Image.open('ring2.png').convert('1')
        		disp.image(img)
        		disp.diplay()
        		time.sleep(0.5)
        		
			disp.clear()
        		GPIO.output(buzzer,GPIO.LOW)
        		img=Image.open('ring3.png').convert('1')
        		disp.image(img)
        		disp.diplay()
			time.sleep(0.5)
	print ("Distance measured by sensor is  %.2f" % distance)
	#sleep 0.5 seconds before the next reading
	time.sleep(0.5)
		
		
    

        
      
      
    
    
