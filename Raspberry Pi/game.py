#!/usr/bin/env python

###########################
# imports
###########################

# System   
import os
import serial
from gpiozero import Button
from chessGame import *

# GPIO functions
from RPLCD.i2c import CharLCD
from gpioUtils.powerInterrupt import *
from gpioUtils.Generalized_Diff_test import *
from gpioUtils.difficultyWaitForPress import *
import RPi.GPIO as GPIO
import time

# initialize LCD 
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)
              
###########################
# gpio setup
###########################
button1 = 36
button2 = 40
addr = 0x48
A0 = 0x40
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button2, GPIO.RISING,
		      callback=button_press_callback,
		      bouncetime=7000)
setup_LEDs()
play = "yes"
reset = "yes"

while (play == "yes" and reset == "yes") :
  # ask user if board is reset
  reset = resetWaitForPress()
  
  # play a game of chess
  playChess()
  
  # ask user to play again
  play = playWaitForPress();

stop_LED()		
GPIO.cleanup()
