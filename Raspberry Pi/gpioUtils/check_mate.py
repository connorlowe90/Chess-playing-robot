# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This file checks game states of the board and 
# updates the LCD and LED according to the game state 

from RPLCD.i2c import CharLCD
from Light_Outputs import *
import time
import os
from soundFiles.playSound import * 

# Chess game/engine
import chess

# Setup LCD screen
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)

# Called after each move to see if one of the 
# players are in check, checkmate, stalemate, or draw
def check_game_state(board):
    if(board.is_stalemate()):
        playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/stalemate.wav') 
        stalemate_state()
        return "Stalemate"
    elif(board.can_claim_draw() or board.is_insufficient_material()):
        playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/draw.wav') 
        draw_state()
        return "Draw"
    elif(board.turn == chess.WHITE):
        if(board.is_checkmate()):
            playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/checkmate.wav') 
            check_mate()
            return "Checkmate"
        elif(board.is_check()):
            playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/check.wav') 
            in_check()
            return "Running"
    elif(board.turn == chess.BLACK):
        if(board.is_checkmate()):
            playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/checkmate.wav') 
            check_mate_comp()
            return "Checkmate"
        elif(board.is_check()):
            playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/check.wav') 
            in_check_comp()
            return "Running"
    return "Running"
          
def check_game_state_s(board, promotion):
    if(board.is_stalemate()):
        light_pink_LED()
        playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/stalemate.wav') 
        return stalemate_s()
    elif(board.can_claim_draw() or board.is_insufficient_material()):
        cyan_LED()
        playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/draw.wav') 
        return draw_state_s()
    elif(board.is_checkmate()):
        green_LED()
        playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/checkmate.wav') 
        return check_mate_s()
    elif(board.is_check()):
        purple_LED()
        playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/check.wav') 
        return in_check_s()
    elif(promotion):
        playSound('/home/pi/Embedded-Capstone/gpioUtils/soundFiles/promote.wav') 
        return "Promote to Queen"
    
        
# check_mate() function is for when
# the computer has the user in check
# mate. Once you are in check mate
# the LCD will clear what is on it,
# say you lost, and the RGB LED will
# will flash red.
def check_mate():
    lcd.clear()
    lcd.write_string('Checkmate\r\nYou lost')
    loser()
    lcd.clear()
    
def check_mate_s():
    return "Im in checkmate"

# in_ckech() function is for when the
# computer has the user in check. Once
# you are in check the LCD will clear
# what is has on it, tell you to protect
# the king, and the RGB LED will flash
# orange.
def in_check():
    lcd.clear()
    lcd.write_string('You are in check\r\nProtect the king')
    user_in_check()
    lcd.clear()
    
def in_check_s():
    return "I'm in check"
    

# check_mate_comp() function is a function
# that is called once the user puts the
# computer in check mate. The LCD will
# clear, print you win, and the RGB LED
# will flash green.
def check_mate_comp():
    lcd.clear()
    lcd.write_string('Checkmate\r\nYou won')
    winner()
    lcd.clear()

# in_check_comp() function is a function
# that is called once the user puts the
# computer in check. The LCD will clear,
# print that they put the comp in check
# and the RGB LED will be purple.
def in_check_comp():
    lcd.clear()
    lcd.write_string('You put me\r\nin check')
    comp_in_check()
    lcd.clear()

# draw_state() function is a function that
# is called once the game is in a draw state.
# The LCD will clear, say that there is a
# draw, and they RGB LED will flash cyan.
def draw_state():
    lcd.clear()
    lcd.write_string('It\'s a draw\r\nGood game')
    got_a_draw()
    lcd.clear()
    
def draw_state_s():
    return "It's a draw"

# stalemate() function is a function that
# is called once there is a stalemate.
# The LCD will clear, say there is a stalemate
# and the RGB LED will flash light pink and
# orange
def stalemate_state():
    lcd.clear()
    lcd.write_string('It\'s a stalemate\r\nGood game')
    stalemate()
    lcd.clear()
    
def stalemate_s():
    return "Stalemate"

# illegal_move() function is called when the
# user makes and illegal move. The LCD will
# display illegal move and then RGB LED will
# flash red and blue
def illegal_move():
    lcd.clear()
    lcd.write_string('Illegal move')
    illegal_LED()
    #lcd.clear()
    
# comp_moving() function is called when the
# computer is making a move. The LCD will clear,
# a message will be displayed, and the LED will
# be yellow in color for a warning.      
def comp_moving():
    lcd.clear()
    lcd.write_string('I am moving\r\nPlease wait')
    yellow_LED()
    lcd.clear()
