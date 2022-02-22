#!/usr/bin/env python

###########################
# imports
###########################

# System   
import os
import serial

# Chess game/engine
import chess
import chess.uci
import chess.engine
from chess import *
from stockfish import Stockfish

# engine using stockfish package
stockfish = Stockfish('/home/pi/ee475/Chess-Engines-for-Raspberry-Pi-by-Al-master/arm7l/stockfish231')
print(stockfish.get_best_move())

# Chessboard detection functions
from imgUtils.detectRect import *
from imgUtils.takePic import * 
from imgUtils.boardNotation import *
from imgUtils.imProc import *
from imgUtils.takePicOW import *
from imgUtils.takePicOW2 import *
import cv2
from gpiozero import Button

# GPIO functions
from RPLCD.i2c import CharLCD
from gpioUtils.Light_Outputs import *
from gpioUtils.hintInterrupt import *
from gpioUtils.powerInterrupt import *
from gpioUtils.Generalized_Diff_test import *
from gpioUtils.check_mate import *
from gpioUtils.difficultyWaitForPress import *
import RPi.GPIO as GPIO
import time

# Image path
image_pathStart = r'/home/pi/ee475/calibration/test1.bmp'
image_pathStart2 = r'/home/pi/ee475/calibration/test2.bmp'
image_pathBlank = r'/home/pi/ee475/calibration/blank1.bmp'

###########################
# chess game
###########################

# initialize bluetooth
stm = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=None)

# initialize LCD 
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=False,
              backlight_enabled=True)
              
###########################
# gpio setup
###########################
button1 = 36
button2 = 40
hint_button = 38
addr = 0x48
A0 = 0x40
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Event handler for if someone presses
# the O/F button. The bounce time may
# need to be changed.
GPIO.add_event_detect(button2, GPIO.RISING,
                      callback=button_press_callback,
                      bouncetime=7000)

# hint_press_callback() function is a
# function that is will tell you what
# diff you are at
def hint_press_callback(channel):
	stockfish.set_fen_position(board.fen())
	stockfish.set_skill_level(20)
	edit_me = get_best_move(str(chess.Move.from_uci(stockfish.get_best_move())), board)
	lcd.clear()
	lcd.write_string('Best move is: \r\n' + str(edit_me))
	time.sleep(5)
	lcd.clear()
    
# Event handler for if someone presses
# the hint button. The bounce time may
# need to be changed.
GPIO.add_event_detect(hint_button, GPIO.RISING,
                      callback=hint_press_callback,
                      bouncetime=7000)   
    
# setup LED outputs
setup_LEDs()  # Setup the led pins and pot for it
	
###########################
# initialize game
###########################

# initilize board
board = chess.Board()
print(board)

# get initial pictures
imgBlank, corners = detectRectP(image_pathBlank)
takePicOW()
imgB = detectRectPCorners(image_pathStart, corners)
cv2.imwrite(image_pathStart, imgB)

# get difficulty level
diff = difficultyWaitForPress(stockfish)
	
# start game
while 1:
	  
	# wait for button press
	#button.wait_for_press()
	# wait for done signal
	#stm.read(1)
	waitForUserToMovePress()
	
	# get before picture. imgB = before, imgA = after
	imgB = cv2.imread(image_pathStart)
	
	# get corners of new image 
	takePicOW2()
	imgA = detectRectPCorners(image_pathStart2, corners)

	# get move
	move = getMove(imgB, imgA, imgBlank)

	# if user move if valid push else not
	if chess.Move.from_uci(move) in board.legal_moves:
		# user move
		board.push(chess.Move.from_uci(move))
		check_game_state(board)
		
		# computer move
		stockfish.set_skill_level(diff)
		stockfish.set_fen_position(board.fen())
		newMove = stockfish.get_best_move()
		stm.write("{}\n".format(newMove))
		board.push(chess.Move.from_uci(newMove))
		check_game_state(board)
	else:
		newMove = "".join(map(str.__add__, move[-2::-2] ,move[-1::-2]))
		stm.write("{}\n".format(newMove))

	# wait for done signal
	#stm.read(1)
	waitForUserToMovePress()
	
	print(board.fen())
	
	os.system("espeak -s60 \"Ready\"") 
	
	# save new picture as next starting picture after recieving done signal from stm32
	takePicOW2()
	imgA = detectRectPCorners(image_pathStart2, corners)
	cv2.imwrite(image_pathStart, imgA)
    
stop_LED()		
GPIO.cleanup()



