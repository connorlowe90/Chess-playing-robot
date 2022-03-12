# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This file was a testing main for buttons, LED, LCD, and pot

import time
import RPi.GPIO as GPIO
import smbus
from RPLCD.i2c import CharLCD
from interrupt_test import *
from hint_button_interrupt_LCD import *
from check_mate import *
from Set_Diff import *
# from Generalized_Diff_test import *
from Light_Outputs import *   # This may be commented out and not needed
from LCD_Power import *

diff = 0
delta = -1

# Setup LCD screen
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)


setup_LEDs()  # Setup the led pins and pot for it

button1 = 15
button2 = 32
hint_button = 36

addr = 0x48
A0 = 0x40

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Event handler for if someone presses
# the O/F button. The bounce time may
# need to be changed.
GPIO.add_event_detect(button2, GPIO.FALLING,
                      callback=button_press_callback,
                      bouncetime=7000)

# Event handler for if someone presses
# the hint button. The bounce time may
# need to be changed.
GPIO.add_event_detect(hint_button, GPIO.FALLING,
                      callback=hint_press_callback,
                      bouncetime=7000)


bus = smbus.SMBus(1)


# stalemate_state()
# draw_state()
# check_mate_comp()
# in_check_comp()
# check_mate()
# in_check()
illegal_move()

# while(True):
#     diff = getDiffLvl(delta)
#     delta = diff
#     if(GPIO.input(button1) == GPIO.LOW):
#         print("Button1 pressed")
#         diff = getDiffLvl(delta)
#         lcd.clear()
#         break
#     time.sleep(0.4)


print("out of loop")
print("Chose Level:", diff, "\n")
lcd.write_string("Chose Level: " + str(diff))
time.sleep(5)



stop_LED()
lcd.clear()
GPIO.cleanup()