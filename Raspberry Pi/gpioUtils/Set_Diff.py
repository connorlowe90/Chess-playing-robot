# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This was the original test file for setting difficulty
# prior to creating the generalized diff file.

import RPi.GPIO as GPIO
import smbus
from RPLCD.i2c import CharLCD

# Setup LCD screen
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)

# Still need to set warnings to false
# and for now set the board pins for GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Setup for the poteniometer
addr = 0x48
A0 = 0x40

bus = smbus.SMBus(1)


# getDiffLvl() function will take in current diff
# as a parameter and test the potentiometer value
# to choose a difficulty and return that value
#
# param currentDiff:
#    currentDiff is an int that is passed
#    in to hold the current difficulty level
#    based on the potentiometer value
#
# return diff:
#    return the current difficulty in select
def getDiffLvl(currentDiff):
    # Get the bytes for writing and
    # reading from the potentiometer
    bus.write_byte(addr, A0)
    value = bus.read_byte(addr) / 2.55
    
    # If/elif/else statements to test the value
    # and display the difficulty value to the screen
    if(value < 25):
        if(currentDiff != 1):
            lcd.clear()
            lcd.write_string('Difficulty\r\nLevel: 1')
        diff = 1
    elif(25 <= value < 50):
        if(currentDiff != 2):
            lcd.clear()
            lcd.write_string('Difficulty\r\nLevel: 2')
        diff = 2
    elif(50 <= value < 75):
        if(currentDiff != 3):
            lcd.clear()
            lcd.write_string('Difficulty\r\nLevel: 3')
        diff = 3
    else:
        if(currentDiff != 4):
            lcd.clear()
            lcd.write_string('Difficulty\r\nLevel: 4')
        diff = 4
    return diff
