from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time
from Generalized_Diff_test import *

button1 = 36
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)
    
def difficultyWaitForPress():    
  diff = 0
  delta = -1
  while(True):
      diff = getDiffLvl(delta)
      delta = diff
      if(GPIO.input(button1) == GPIO.HIGH):
          diff = getDiffLvl(delta)
          lcd.clear()
          break
      time.sleep(0.4)
  lcd.write_string("Chose Level: " + str(diff))
  time.sleep(5)
  lcd.clear()

def waitForUserToMovePress():
  while(True):  
    if(GPIO.input(button1) == GPIO.HIGH):
      lcd.clear()
      lcd.write_string("Move accepted")
      time.sleep(0.5)
      lcd.clear()
      break
