# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This file is for powering on/off the LCD screen

from RPLCD.i2c import CharLCD
from Light_Outputs import no_LED
import time

# Setup LCD screen
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)

# power_off() function will clear the LCD screen,
# write "Powering Off" to the screen, pause for
# 5 seconds, clear the screen and have LCD
# backlight be turned to false
def power_off():
    no_LED()
    lcd.clear()
    lcd.write_string('Powering Off')
    time.sleep(5)
    lcd.clear()
    CharLCD(i2c_expander='PCF8574', address=0x27, backlight_enabled=False)
    
    
# power_on() function will clear the LCD screen,
# write "Powering On" to the screen, pause for
# 5 seconds, clear the screen and have LCD
# backlight be turned to true
def power_on():
    lcd.clear()
    lcd.write_string('Powering On')
    time.sleep(5)
    lcd.clear()
    CharLCD(i2c_expander='PCF8574', address=0x27, backlight_enabled=True)
    
