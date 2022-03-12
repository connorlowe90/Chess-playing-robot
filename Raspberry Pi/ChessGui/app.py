#!/usr/bin/env python3
from simplejson import JSONDecodeError
from socket import socket
from flask import Flask, request
from flask import render_template
from flask_socketio import SocketIO, send, emit
import chess.engine
import chess
import logging, sys
from stockfish import Stockfish
from imgUtils.boardNotation import formatMove, check_captured_moveWhite, getPieceIndex, getMoveBlackIndices  
import serial
from gpioUtils.Light_Outputs import setup_LEDs 
import time

stockfish = Stockfish('/home/pi/Embedded-Capstone/Chess-Engines-for-Raspberry-Pi-by-Al-master/arm7l/stockfish231')


app = Flask(__name__, template_folder="templates")

HtmlFile = open('IntroMessage.html')
source_code = HtmlFile.read() 
board = chess.Board()
stm = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=None)
setup_LEDs()


@app.route('/Group5ChessRobot')
def route():
    return source_code


@app.route('/make_move', methods=['POST'])
def make_move():
    # User move
    usrMove = request.form.get('userMove')
    pieceCap, moveOutFrom, moveOutTo = check_captured_moveWhite(usrMove[2:], board)

    toSTM = ""
    
    # Castling
    if (board.has_kingside_castling_rights(chess.WHITE) and usrMove[2:] == "e1g1"):
        toSTM = str(2) + ',' + str(0) + ',' + str(2) + '/'
    elif (board.has_queenside_castling_rights(chess.WHITE) and usrMove[2:] == "e1c1"):
        toSTM = str(2) + ',' + str(7) + ',' + str(4) + '/'
            
    # Captured move off board
    if (pieceCap != "none"):
        pieceCap = getPieceIndex(pieceCap)
        toSTM = str(toSTM) + str(pieceCap) + ',' + str(moveOutFrom) + ',' + str(moveOutTo) + '/'
    
    # Captured move on board
    indexesOut = [usrMove[2:][i:i+2] for i in range(0, len(usrMove[2:]), 2)]
    piece2, move21, move22 = getMoveBlackIndices(board, indexesOut)
    toSTM = str(toSTM) + str(piece2) + ',' + str(move21) + ',' + str(move22) + '/$'
    print(toSTM)
    stm.write("{}\n".format(toSTM))
    
    # wait for done signal
    readstring = ''
    while (readstring.find("Move Complete") == -1) :
        c = stm.read(1)
        readstring = readstring + c
        print(readstring)
    
    time.sleep(1)
    
    # Computer move
    fen = request.form.get('fen')
    toSTM = ""
    toSTM, newMove = formatMove(board, stockfish, str(usrMove[2:]), 0)
    print(toSTM)
    stm.write("{}\n".format(toSTM))
    
    # Wait for done signal
    if (newMove != 1):
			# wait for done signal
		readstring = ''
		while (readstring.find("Move Complete") == -1) :
			c = stm.read(1)
			readstring = readstring + c
			print(readstring)
    
    # Debug
    fen = board.fen()
    print(fen)
    
    # Fen to print to board
    return fen



if __name__ == '__main__':
    app.run(host='0.0.0.0')
