# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This file implements a hint button for the user

from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO
import time
import chess

# Rank and file arrays for piece location
dArray1 = [1, 2, 3, 4, 5, 6, 7, 8]
dArray2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
dArray3 = [7, 6, 5, 4, 3, 2, 1, 0]

# GPIO pin 38 setup for hint button
button = 38
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Setup LCD screen
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)

# get_best_move() function will get the best move
# for the user. This function takes in 'move' and
# 'board' as parameters, and will check for the best
# move in the currecnt board state.    
def get_best_move(move, board):
    moveArray = []
    
    # Append 'i' for a move into moveArray
    for i in move:
      moveArray.append(i)
    
    # Get the file (column)
    for i in range(0, 8):
      if(moveArray[0] == dArray2[i]):
        moveArray[0] = dArray1[i] - 1
    
    # Get the rank (row)
    # get the piece at the location 
    moveArray[1] = int(moveArray[1]) - 1
    piece = board.piece_at(chess.square(int(moveArray[0]), int(moveArray[1])))
    
    fullPiece = ''
    
    # Check for the piece letter and assign the
    # piece name for that letter to fullPiece
    if(str(piece) == 'n' or str(piece) == 'N'): 
        fullPiece = "Kinght"
    elif(str(piece) == 'k' or str(piece) == 'K'):
        fullPiece = "King"
    elif(str(piece) == 'q' or str(piece) == 'Q'):
        fullPiece = "Queen"
    elif(str(piece) == 'p' or str(piece) == 'P'):
        fullPiece = "Pawn"
    elif(str(piece) == 'b' or str(piece) == 'B'):
        fullPiece = "Bishop"
    elif(str(piece) == 'r' or str(piece) == 'R'):
        fullPiece = "Rook"
    position = ''.join(moveArray[2:4])
    
    # Concatenate fullMove with the piece to
    # to square to move the piece to and return
    # the full move. 
    fullMove = fullPiece + " to " + position
    return fullMove
