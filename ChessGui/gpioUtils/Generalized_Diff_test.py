import RPi.GPIO as GPIO
import smbus
from RPLCD.i2c import CharLCD
from numpy import interp

# Need to bring the LCD in for now.
# Might be able to fix that by passing
# a parameter or something
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)

# Still need to set warnings to false
# and for now set the board pins for GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Setup for the LCD with I2C
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
    value = int(bus.read_byte(addr))
    diff = int(mapD(value, 0, 192, 1, 4))

    # If/elif/else statements to test the value
    # and display the difficulty value to the screen
    if(currentDiff != diff):
        lcd.clear()
        lcd.write_string('Difficulty\r\nLevel: ' + str(diff))
    return diff
    
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

def mapD(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
