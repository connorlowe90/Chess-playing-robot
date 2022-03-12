# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# This file is for dealing with board notation for
# piece locations, captured/capaturing pieces, castling, 
# player moves.

import chess
import sys
sys.path.insert(1, '//home/pi/Embedded-Capstone')
from gpioUtils.Light_Outputs import *
from gpioUtils.check_mate import *
from gpioUtils.difficultyWaitForPress import *
from imgUtils.imProc import *

# constant chessboard notation
# our index 0-63
chessboard = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
		 'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
		 'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
		 'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
		 'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
		 'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
		 'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
		 'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
		 'pp1', 'pp2', 'pp3', 'pp4', 'pp5', 'pp6', 'pp7', 'pp8',
		 'rr1', 'nn1', 'bb1', 'qq1', 'kk1', 'bb2', 'nn2', 'rr2',
		 'qq2']

# each indexed 0-16		 
noncapWhite = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8',
			  'r1', 'n1', 'b1', 'q1', 'k1', 'b2', 'n2', 'r2',
			  'q2']
noncapBlack = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8',
			  'r1', 'n1', 'b1', 'q1', 'k1', 'b2', 'n2', 'r2',
			  'q2']
			  
pieceSymbolNums = ['p', 'n', 'r', 'b', 'q', 'k'] 

# lists for captured pieces to be added to  
capWhite = []
capBlack = []
	
dArray1 = [1, 2, 3, 4, 5, 6, 7, 8]
dArray2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
dArray3 = [7, 6, 5, 4, 3, 2, 1, 0]
	 
# returns chessboard notation given index starting at a8
def indexToBoardNotation(index):
	return chessboard[index]

# returns index that corrosponds to index on STM board
def returnIndexSTM(index):
	return 63 - index
	
# return index of given square in given array
def returnIndexOf(square, array):
	c = 0
	for i in array:
		if i == square:
			return c
		c += 1
			
# gets number of captured piece to determine where to put next
def getPieceIter(piece, array):
	c = 0
	for i in array:
		if i == piece:
			c = c + 1
	return c

# check_captured_move() is a function that
# checks to see if a piece is captured 
def check_captured_move(move, board):
    moveArray = []
    moveArray2 = []
    print(move)
    
    for i in move:
      moveArray.append(i)
      moveArray2.append(i)
    
    for i in range(0, 8):
      if(moveArray[2] == dArray2[i]):
        moveArray[2] = dArray1[i] - 1
      
    moveArray[3] = int(moveArray[3]) - 1
    pieceCap = board.piece_at(chess.square(int(moveArray[2]), int(moveArray[3])))
    pieceCap = str(pieceCap).lower() 

    if (pieceCap != None):
        # start position
        startPosition = ''.join(moveArray2[2:4])
        fromIndex = returnIndexSTM(returnIndexOf(startPosition, chessboard))
        
        # ending position
        capWhite.append(pieceCap)
        count = getPieceIter(pieceCap, capWhite)
        endPosition = str(pieceCap) + str(pieceCap) + str(count)
        
        # changed non cap white to chessboard
        toIndex = returnIndexOf(endPosition, chessboard)
        return pieceCap, fromIndex, toIndex	
    
    return None, None. None
	
# get formated indexes for sending to STM for black move	
def getMoveBlackIndices(board, indexOut):
	# getting piece
	fmoveArray = []
	for i in indexOut[0]:
		fmoveArray.append(i)
	  
	for i in range(0, 8):
		if(fmoveArray[0] == dArray2[i]):
			fmoveArray[0] = dArray1[i] - 1
	fmoveArray[1] = int(fmoveArray[1]) - 1
	piece = board.piece_at(chess.square(int(fmoveArray[0]), int(fmoveArray[1])))
	pieceIndex = returnIndexOf(str(piece).lower(), pieceSymbolNums)

	# getting indexes
	indexy1 = returnIndexSTM(returnIndexOf(indexOut[0], chessboard))
	indexy2 = returnIndexSTM(returnIndexOf(indexOut[1], chessboard))
	return pieceIndex, indexy1, indexy2

def getPieceIndex(piece):
	return returnIndexOf(str(piece), pieceSymbolNums)
	
def checkCastlingMove(board, A, castling, imgA, imgB, imgBlank):
	move = ''
	if (A != None and (board.has_kingside_castling_rights(chess.WHITE)
		or  board.has_queenside_castling_rights(chess.WHITE))):
		if (board.has_kingside_castling_rights(chess.WHITE) and
			str(60) in castling and str(61) in castling and
			str(62) in castling and str(63) in castling):
			move = 'e1g1'
		elif (board.has_queenside_castling_rights(chess.WHITE) and
			str(60) in castling and str(58) in castling and
			str(56) in castling and str(59) in castling):
			move = 'e1c1'
	else :	
		# get move
		move = getMove(imgB, imgA, imgBlank)
	return move
	
def formatMove(board, stockfish, move, diff):
	# if user move if valid push else not
	print(move)
	if (chess.Move.from_uci(move) in board.legal_moves or 
		chess.Move.from_uci(move + "q") in board.legal_moves):
			
		# checking promotion always to queen 
		if (chess.Move.from_uci(move + "q") in board.legal_moves) :
			piecePromoted = promotionWaitForPress()
			move = move + piecePromoted
			
		# default led status while moving
		yellow_LED()
		
		# user move
		board.push(chess.Move.from_uci(move))
		
		# computer move
		stockfish.set_skill_level(diff)
		stockfish.set_fen_position(board.fen())
		
		newMove = stockfish.get_best_move()
		
		# Sending to STM
		toSTM = ''
		promotion = 0
		newMove2 = newMove
		# check if castling occured and add a corrosponding rook move
		# check if stockfish is promoting 
		if (board.has_kingside_castling_rights(chess.BLACK) and newMove == "e8g8"):
			toSTM = str(2) + ',' + str(56) + ',' + str(58) + '/'
		elif (board.has_queenside_castling_rights(chess.BLACK) and newMove == "e8c8"):
			toSTM = str(2) + ',' + str(63) + ',' + str(60) + '/'
		elif (newMove.find('q') == 4) :
			promotion = 1
			newMove2 = newMove[:-1]
		
		pieceCap, moveOutFrom, moveOutTo = check_captured_move(newMove2, board)
    
		# captured move off board
		if (pieceCap != "none"):
			pieceCap = getPieceIndex(pieceCap)
			toSTM = str(toSTM) + str(pieceCap) + ',' + str(moveOutFrom) + ',' + str(moveOutTo) + '/'
		
		# captured move on board
		indexesOut = [newMove2[i:i+2] for i in range(0, len(newMove2), 2)]
		piece2, move21, move22 = getMoveBlackIndices(board, indexesOut)
		toSTM = str(toSTM) + str(piece2) + ',' + str(move21) + ',' + str(move22) + '/$'
		print("hello")
		print(board.fen())
		# printing to lcd
		state = check_game_state_s(board, promotion)
		
		if (state == "Im in checkmate" or
			state == "It's a draw" or
			state == "Stalemate") :
				return '', 1
		lcd.clear()
		if (state != None) :
			lcd.write_string('Making a move\r\n' + state)
		else :
			lcd.write_string('Making a move\r\n')
			
		board.push(chess.Move.from_uci(newMove))
		
		# push captured move
		return toSTM, newMove
	else:	
		# Sending to STM
		toSTM = ''
		indexesOut = [move[i:i+2] for i in range(0, len(move), 2)]
		piece2, move21, move22 = getMoveBlackIndices(board, indexesOut)
		newMove = "".join(map(str.__add__, move[-2::-2] ,move[-1::-2]))
		indexesOut = [newMove[i:i+2] for i in range(0, len(newMove), 2)]
		piece3, move21, move22 = getMoveBlackIndices(board, indexesOut)
		toSTM = str(toSTM) + str(piece2) + ',' + str(move21) + ',' + str(move22) + '/$'
		return toSTM, None

# getMove() is a function that gets user move 
# from 2 images
def getMove(imgB, imgA, imgBlank):
	# window slide and save 64 images X 2 (before and after)
	imgASlide, imgBSlide = getImgSlide(imgA, imgB)
	imgA2Slide, imgBlankSlide = getImgSlide(imgA, imgBlank)  

	# analyze slide	
	ssimArray = analyzeSlide(imgASlide, imgBSlide)
	ssimArrayBlank = analyzeSlide(imgA2Slide, imgBlankSlide)

	index1, index2 = find2Mins(ssimArray)

	boardNotation1 = indexToBoardNotation(index1)
	boardNotation2 = indexToBoardNotation(index2)

	if ssimArrayBlank[index1] > ssimArrayBlank[index2]:
		return boardNotation1 + boardNotation2
	else:
		return boardNotation2 + boardNotation1
