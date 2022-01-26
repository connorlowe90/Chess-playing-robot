#!/usr/bin/env python

###########################
# imports
###########################

# System
import os

# Chess game/engine
import chess
from chess import *
import chess.engine
import chess.uci
from stockfish import Stockfish

# engine using stockfish package
stockfish = Stockfish('/home/pi/ee475/Chess-Engines-for-Raspberry-Pi-by-Al-master/arm7l/t-fruit')

# bluetooth
import serial

# image processing
import numpy as np
import cv2
from skimage import data,io,filters
from skimage.measure import compare_ssim as ssim

# Chessboard detection
from detectRect import *
from takePic import *

###########################
# functions
###########################

# initialize bluetooth
stm = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
# ~ stm.write('Bc5\n')
# ~ result=stm.read(100)
# ~ print (result)

# initilize board
board = chess.Board()

# detect chessboard from picture. imgB = before, imgA = after
imgB = detectRectP('/home/pi/ee475/camCal/calibration/start.png')
# ~ imgA = detectRectI(takePic())

cv2.imshow('img', imgB)
cv2.waitKey(1000)
imgA = takePic()
cv2.imshow('img', imgA)
cv2.waitKey(1000)

# window slide and save 64 images X 2 (before and after)
imgASlide = []
imgBSlide = []
for i in range(0, len(imgB), 64):
	for j in range(0, len(imgB[0]), 64):
		img2 = np.zeros((64,64,3))
		img2 = imgA[i:i+64,j:j+64]
		imgASlide.append(img2)
		img2 = np.zeros((64,64,3))
		img2 = imgB[i:i+64,j:j+64]
		imgBSlide.append(img2)

for i in range(0, 64):
	cv2.imshow('img', imgBSlide[i])
	cv2.waitKey(200)

# analyze slide	
possiblyMoved = np.zeros(64)
for i in range(0, 64):
	mssim = ssim(imgBSlide[i], imgASlide[i], multichannel=True)
	if mssim < 0.6:
		possiblyMoved[i] = 1

# test moves
Nf3 = chess.Move.from_uci("g1f3")
board.push(Nf3)
print(board)

# check legal move
print(board.legal_moves) 
print(chess.Move.from_uci("a8a1") in board.legal_moves)

# get best move
stockfish.set_fen_position(board.fen())
print(stockfish.get_best_move())
