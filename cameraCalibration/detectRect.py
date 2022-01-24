# imports 
import cv2
import numpy as np
import glob

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

chessboardSize = (7,7)
frameSize = (330,640)

# Using cv2.imread() method
img = cv2.imread('/home/pi/ee475/camCal/calibration/test2.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Find the chess board corners
ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

# output image size
width, height = 512,512

# warp perspective
offset = 25
corners[0] = [corners[0][0][0]-offset,corners[0][0][1]-offset]
corners[6] = [corners[6][0][0]+offset,corners[6][0][1]-offset]
corners[42] = [corners[42][0][0]-offset,corners[42][0][1]+offset]
corners[48] = [corners[48][0][0]+offset,corners[48][0][1]+offset]

pts1 = np.float32([corners[0],corners[6],corners[42],corners[48]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOutput = cv2.warpPerspective(img,matrix,(width,height))

# output
cv2.imwrite('./proccessing/caliResult1.png', imgOutput)
