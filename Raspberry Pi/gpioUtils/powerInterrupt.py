# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This file is for the power button interrupt to
# control the LCD backlight.

import RPi.GPIO as GPIO
import time
from LCD_Power import*

# Setup GPIO pin 40 for the LCD power button.
# Have count be 1 to start for LCD in on state 
# to start. 
button = 40
count = 1

# Button setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# button_press_callback() is a function that
# is called when the power button is pressed
# and checks to see if count the value of count
# and turns the LCD on, or off accordingly. 
def button_press_callback(channel):
    global count
    time.sleep(1)
    if(count == 1):
        power_off()
        count = 0
    else:
        power_on()
        count = 1
    
    
    
    

