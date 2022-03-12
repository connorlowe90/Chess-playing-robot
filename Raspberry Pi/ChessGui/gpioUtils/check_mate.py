from RPLCD.i2c import CharLCD
from Light_Outputs import *
import time
import os

# Chess game/engine
import chess

# Need to bring the LCD in for now.
# Might be able to fix that by passing
# a parameter or something
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)

# Called after each move to see if one of the 
# players are in check, checkmate, stalemate, or draw
def check_game_state(board):
    if(board.is_stalemate()):
        os.system("espeak -s60 \"Stalemate\"") 
        stalemate_state()
        return "Stalemate"
    elif(board.can_claim_draw() or board.is_insufficient_material()):
        os.system("espeak -s60 \"Draw\"") 
        draw_state()
        return "Draw"
    elif(board.turn == chess.WHITE):
        if(board.is_check()):
            os.system("espeak -s60 \"Check\"") 
            in_check()
            return "Running"
        elif(board.is_checkmate()):
            os.system("espeak -s60 \"Checkmate\"") 
            check_mate()
            return "Checkmate"
    elif(board.turn == chess.BLACK):
        if(board.is_check()):
            os.system("espeak -s60 \"Check\"") 
            in_check_comp()
            return "Running"
        elif(board.is_checkmate()):
            os.system("espeak -s60 \"Check\"") 
            check_mate_comp()
            return "Checkmate"
    return "Running"
            
def check_game_state_s(board, promotion):
    if(board.is_stalemate()):
        light_pink_LED()
        os.system("espeak -s60 \"Stalemate\"") 
        return stalemate_s()
    elif(board.can_claim_draw() or board.is_insufficient_material()):
        cyan_LED()
        os.system("espeak -s60 \"Draw\"") 
        return draw_state_s()
    elif(board.is_check()):
        purple_LED()
        os.system("espeak -s60 \"Check\"") 
        return in_check_s()
    elif(board.is_checkmate()):
        green_LED()
        os.system("espeak -s60 \"Checkmate\"") 
        return check_mate_s()
    elif(promotion):
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
    
    
def comp_moving():
    lcd.clear()
    lcd.write_string('I am moving\r\nPlease wait')
    yellow_LED()
    lcd.clear()
