# Kellen Hartnett
# Adrian Lewis
# Connor Lowe
# Sahibjeet Singh
# Garrett Tashiro
# EE 475, Group 5 Capstone Project
# Interpolates points given corners of a chessboard

import numpy as np

# array length function
def array_length(a):
    counter = 0
    for char in a:
        counter += 1
    return counter

# setting up interpolation between 4 corner points
h1 = [60, 169]
a1 = [57, 455]
h8 = [345, 166]
a8 = [341, 453]
board = np.zeros((8, 8, 2))
board2 = np.zeros((8, 8, 2))
board3 = np.zeros((8, 8, 2))
board[0][0]  = h1
board[0][7]  = a1
board[7][0] = h8
board[7][7] = a8

# Horizontal interpolation
for i in range(0, 8):
    for j in range (1, 7):
        board[i][j][0] = (board[i][0][0] * ((7-j)/7)) + (board[i][7][0] * (j/7)) 
        board[i][j][1] = (board[i][0][1] * ((7-j)/7)) + (board[i][7][1] * (j/7))

# Vertical interpolation
for i in range(0, 8):
    for j in range(0, 8):
        board2[i][j][0] = (board[0][i][0] * ((7-j)/7)) + (board[7][i][0] * (j/7)) 
        board2[i][j][1] = (board[0][i][1] * ((7-j)/7)) + (board[7][i][1] * (j/7))
        
# rotation
for i in range(0, 8):
    for j in range(0, 8):
        board3[i][j] = board2[j][i]
                
# Printing 
np.set_printoptions(threshold=np.inf)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print("chessboard = \n", board2)
print("chessboard2 = \n", board3)

# setting up interpolation between 4 corner points
p1 = [57, 91]
p8 = [343, 89]
r1 = [59, 50]
r2 = [343, 49]
q2 = [383, 69]
captured = np.zeros((8, 2, 2))
captured2 = np.zeros((8, 2, 2))
captured[0][0] = p1
captured[7][0] = p8
captured[0][1] = r1
captured[7][1] = r2

# Vertical interpolation
for i in range(1, 7):
    for j in range(0, 2):
        captured[i][j][0] = (captured[0][j][0] * ((7-i)/7)) + (captured[7][j][0] * (i/7)) 
        captured[i][j][1] = (captured[0][j][1] * ((7-i)/7)) + (captured[7][j][1] * (i/7))
                
# Printing 
np.set_printoptions(threshold=np.inf)
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
print("\ncaptured = \n", captured)
print("\nq2 = \n", q2)