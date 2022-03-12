# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This file is implementing the potentiometer for selecting
# difficulty, promotion pieces, if user wants to play, if 
# the board is ready, as well as waiting for user button
# press and setting the chess engine difficulty.

from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time
from Generalized_Diff_test import *

# Setup GPIO pin 36 for accept button
button1 = 36
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Difficulty array for stockfish engine
diffArray = [0, 2, 4, 6]

# Setup LCD screen
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)

# difficultyWaitForPress() function takes in
# stockfish engine as a parameter and calls 
# getDiffLvl() to change difficulty using the
# potentiometer. This funciton will return the
# difficulty level for teh stockfish engine. 
def difficultyWaitForPress(stockfish):    
  diff = 0
  delta = -1
  
  # Stay in while loop until button is pressed 
  # to accept the difficulty level. Update diff
  # to the new value from getDiffLvl() and update 
  # delta. 
  while(True):
      diff = getDiffLvl(delta)
      delta = diff
      if(GPIO.input(button1) == GPIO.HIGH):
          diff = getDiffLvl(delta)
          setDiff(diffArray[diff-1], stockfish)
          lcd.clear()
          break
      time.sleep(0.4)
  
  # Update the LCD screen for the selected level
  # and return the difficulty. 
  lcd.write_string("Chose Level: " + str(diff))
  time.sleep(5)
  lcd.clear()
  return diff

# promotionWaitForPress() is a function that
# uses the potentiometer to select the piece
# you are promoting a pawn to, and will return 
# the selected piece to be pushed to the board.  
def promotionWaitForPress():    
  diff = 0
  delta = -1
  
  # Stay in loop until button is pressed
  # to accept promotion. 
  while(True):
      promotion = getPromotion(delta)
      delta = promotion
      if(GPIO.input(button1) == GPIO.HIGH):
          promotion = getPromotion(delta)
          lcd.clear()
          break
      time.sleep(0.4)
      
      # Check for piece promotion type
      if (promotion == 'q') :
        promotion2 = 'Queen'
      elif (promotion == 'r') :
        promotion2 = 'Rook'
      elif (promotion == 'n') :
        promotion2 = 'Night'
      elif (promotion == 'b') :
        promotion2 = 'Bishop'
  
  # Display what the piece is being promoted to
  lcd.write_string("Promoting to: \r\n" + str(promotion2))
  time.sleep(5)
  lcd.clear()
  return promotion

# playWaitForPress() is a function that is 
# called prior to reentering a new game. 
def playWaitForPress():    
  diff = 0
  delta = -1
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  
  # Stay in while loop until button is 
  # pressed to determine if the game will
  # be played again.
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

# resetWaitForPress()
def resetWaitForPress():    
  diff = 0
  delta = -1
  
  # Stay in while loop until button is 
  # pressed for if the board is ready
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

# waitForUserToMovePress() function wait for
# a button press from the user to tell the
# system the user is done making a move.
def waitForUserToMovePress():
  while(True):  
    if(GPIO.input(button1) == GPIO.HIGH):
      lcd.clear()
      lcd.write_string("Move accepted")
      time.sleep(0.5)
      lcd.clear()
      break

# Set the diff level for the stockfish
# chess engine.      
def setDiff(diff, stockfish):
  stockfish.set_skill_level(diff)
  stockfish.get_skill_level()
