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
from imgUtils.boardNotation import *
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
stm = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=None)

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
    
# setup LED outputs
	
###########################
# initialize game
###########################
def playChess():
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
						  
	# initilize board
	#setup_LEDs()  # Setup the led pins and pot for it
	board = chess.Board()
	board.set_fen("r3kb1r/pppqpppp/3p1nb1/3P4/2n1PP2/2N2BP1/PPP4P/R1BQK1NR w KQkq - 3 9")
	print(board)
	legal_moves = list(board.legal_moves)
	print(legal_moves)

	# get initial pictures
	imgBlank, corners = detectRectP(image_pathBlank)
	takePicOW()
	imgB = detectRectPCorners(image_pathStart, corners)
	cv2.imwrite(image_pathStart, imgB)

	# get difficulty level
	diff = difficultyWaitForPress(stockfish)
		
	# State of game
	currentGameState = "Running"
		
	###########################
	# run game
	###########################
	while (currentGameState == "Running"):
		os.system("espeak -s60 \"Ready\"") 
		print(board.fen())
		  
		# wait for user to accept move
		waitForUserToMovePress()

		# get before picture. imgB = before, imgA = after
		imgB = cv2.imread(image_pathStart)

		# get corners of new image 
		takePicOW2()
		imgA = detectRectPCorners(image_pathStart2, corners)

		# getting best move 
		A, B, C, D, castling = find4Mins(imgA, imgB, imgBlank, 0.5)
			
		# Check castling 		
		move = checkCastlingMove(board, A, castling, imgA, imgB, imgBlank)

		# format move for sending to stm takes into acount invalid moves.
		toSTM, newMove = formatMove(board, stockfish, move, diff)
		if (newMove != 1):
			stm.write("{}\n".format(toSTM))
		print(toSTM)
		
		# illegal move
		if (newMove == None) :
			illegal_move()
		
		if (newMove != 1):
			# wait for done signal
			readstring = ''
			while (readstring.find("Move Complete") == -1) :
				c = stm.read(1)
				readstring = readstring + c
				print(readstring)
			
		# make sure game is in a valid state
		currentGameState = check_game_state(board)

		# clear lcd turn off led
		lcd.clear()
		no_LED()
		
		# save new picture as next starting picture after recieving done signal from stm32
		takePicOW2()
		imgA = detectRectPCorners(image_pathStart2, corners)
		cv2.imwrite(image_pathStart, imgA)
		



