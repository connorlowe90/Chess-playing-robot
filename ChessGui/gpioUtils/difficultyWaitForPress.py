from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time
from Generalized_Diff_test import *

button1 = 36
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

diffArray = [0, 2, 4, 6]

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)
    
def difficultyWaitForPress(stockfish):    
  diff = 0
  delta = -1
  while(True):
      diff = getDiffLvl(delta)
      delta = diff
      if(GPIO.input(button1) == GPIO.HIGH):
          diff = getDiffLvl(delta)
          setDiff(diffArray[diff-1], stockfish)
          lcd.clear()
          break
      time.sleep(0.4)
  lcd.write_string("Chose Level: " + str(diff))
  time.sleep(5)
  lcd.clear()
  return diff
  
def promotionWaitForPress():    
  diff = 0
  delta = -1
  while(True):
      promotion = getPromotion(delta)
      delta = promotion
      if(GPIO.input(button1) == GPIO.HIGH):
          promotion = getPromotion(delta)
          lcd.clear()
          break
      time.sleep(0.4)
      if (promotion == 'q') :
        promotion2 = 'Queen'
      elif (promotion == 'r') :
        promotion2 = 'Rook'
      elif (promotion == 'n') :
        promotion2 = 'Night'
      elif (promotion == 'b') :
        promotion2 = 'Bishop'
  lcd.write_string("Promoting to: \r\n" + str(promotion2))
  time.sleep(5)
  lcd.clear()
  return promotion
  
def playWaitForPress():    
  diff = 0
  delta = -1
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  while(True):
      promotion = getPlayState(delta)
      delta = promotion
      if(GPIO.input(button1) == GPIO.HIGH):
          promotion = getPlayState(delta)
          lcd.clear()
          break
      time.sleep(0.4)
  lcd.write_string("Reset the board")
  time.sleep(5)
  lcd.clear()
  return promotion

def resetWaitForPress():    
  diff = 0
  delta = -1
  while(True):
      promotion = getResetState(delta)
      delta = promotion
      if(GPIO.input(button1) == GPIO.HIGH):
          promotion = getResetState(delta)
          lcd.clear()
          break
      time.sleep(0.4)
  lcd.write_string("Starting game \r\n")
  time.sleep(2)
  lcd.clear()
  return promotion

def waitForUserToMovePress():
  while(True):  
    if(GPIO.input(button1) == GPIO.HIGH):
      lcd.clear()
      lcd.write_string("Move accepted")
      time.sleep(0.5)
      lcd.clear()
      break
      
def setDiff(diff, stockfish):
  stockfish.set_skill_level(diff)
  stockfish.get_skill_level()
