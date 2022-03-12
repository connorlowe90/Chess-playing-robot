# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This file has has all the functionality for 
# the poteniometer. All functions are called in
# difficultyWaitForPress.py

import RPi.GPIO as GPIO
import smbus
from RPLCD.i2c import CharLCD
from numpy import interp

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

# Setup for the potentiometer with I2C
addr = 0x48
A0 = 0x40

# Setup the smbus for the potentiometer
bus = smbus.SMBus(1)


# getDiffLvl() function will take in current diff
# as a parameter and test the potentiometer value
# to choose a difficulty and return that value.
# param currentDiff is an int that is passed in to 
# hold the current difficulty level based on the 
# potentiometer value. The function returns the 
# difficulty. 
def getDiffLvl(currentDiff):
    # Get the bytes for writing and
    # reading from the potentiometer
    bus.write_byte(addr, A0)
    value = int(bus.read_byte(addr))
    diff = int(mapD(value, 0, 192, 1, 4))

    # If/elif/else statements to test the value
    # and display the difficulty value to the screen
    if(currentDiff != diff):
        lcd.clear()
        lcd.write_string('Difficulty\r\nLevel: ' + str(diff))
    return diff

# getPromotion() is a function that will use
# the potentiometer to get the piece the user 
# wishes to promote their pawn to. This function
# takes in parameter currentDiff which is associated
# to a letter for the piece the user is choosing. 
# It returns the the piece letter for promotion.   
def getPromotion(currentDiff):
    # Get the bytes for writing and
    # reading from the potentiometer
    bus.write_byte(addr, A0)
    value = bus.read_byte(addr) / 2.55
    
    # If/elif/else statements to test the value
    # and display the difficulty value to the screen
    if(value < 25):
        if(currentDiff != 'q'):
            lcd.clear()
            lcd.write_string('Promotion:\r\nQueen')
        diff = 'q'
    elif(25 <= value < 50):
        if(currentDiff != 'r'):
            lcd.clear()
            lcd.write_string('Promotion:\r\nRook')
        diff = 'r'
    elif(50 <= value < 75):
        if(currentDiff != 'n'):
            lcd.clear()
            lcd.write_string('Promotion:\r\nKnight')
        diff = 'n'
    else:
        if(currentDiff != 'b'):
            lcd.clear()
            lcd.write_string('Promotion:\r\nBishop')
        diff = 'b'
    return diff

# getPlayState() is a function that uses the 
# poteniometer to check if the user wants to play
# the game again. This function takes in currentDiff
# as a parameter for checking if the user wants to play
# again or not and returns the 'yes' or 'no' based on
# potentiometer value.    
def getPlayState(currentDiff):
    # Get the bytes for writing and
    # reading from the potentiometer
    bus.write_byte(addr, A0)
    value = bus.read_byte(addr) / 2.55
    
    # If/elif/else statements to test the value
    # and display the difficulty value to the screen
    if(value < 50):
        if(currentDiff != 'yes'):
            lcd.clear()
            lcd.write_string('Play again?\r\nYes')
        diff = 'yes'
    else:
        if(currentDiff != 'no'):
            lcd.clear()
            lcd.write_string('Play again?\r\nNo')
        diff = 'no'
    return diff

# getResetState() is a function for start of the
# game to check if the board is setup and the player 
# is ready to play. This function takes in currentDiff
# as a parameter for 'yes' or 'no' and returns the same 
# strings based on the potentiometer value.   
def getResetState(currentDiff):
    # Get the bytes for writing and
    # reading from the potentiometer
    bus.write_byte(addr, A0)
    value = bus.read_byte(addr) / 2.55
    
    # If/elif/else statements to test the value
    # and display the difficulty value to the screen
    if(value < 50):
        if(currentDiff != 'yes'):
            lcd.clear()
            lcd.write_string('Board ready?\r\nYes')
        diff = 'yes'
    else:
        if(currentDiff != 'no'):
            lcd.clear()
            lcd.write_string('Board ready?\r\nNo')
        diff = 'no'
    return diff

# mapD() is a function that is used for 
# getting the game difficulty. It helps with
# mapping the potentiometer values to be roughly 
# a quarter turn for each of the four level values.
def mapD(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
