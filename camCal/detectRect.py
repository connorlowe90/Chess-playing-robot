# imports 
import cv2
import numpy as np
import glob
from imutils import perspective

########################################################## 
# FIND CHESSBOARD CORNERS - Warp perspective to crop to board 
##########################################################
def detectRectP(path):
	"""Warps perspective to crop picture to chess board.
	path = path to the picture you want to crop
    returns the crppped image that is just the chess board
    """
	chessboardSize = (7,7)
	frameSize = (330,640)
	
	# Using cv2.imread() method
	img = cv2.imread(path)
	
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	# Find the chess board corners
	ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)
	
	# output image size
	width, height = 512,512
	dim = (width, height)
	
	# get corners using inside points and a pixel offset
	offset = 25
	corners[0] = [corners[0][0][0]-offset,corners[0][0][1]-offset]
	corners[6] = [corners[6][0][0]+offset,corners[6][0][1]-offset]
	corners[42] = [corners[42][0][0]-offset,corners[42][0][1]+offset]
	corners[48] = [corners[48][0][0]+offset,corners[48][0][1]+offset]
	
	# cropping/rotation method one - opencv warp perspective
	pts1 = np.array([corners[0],corners[6],corners[42],corners[48]])
	pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
	matrix = cv2.getPerspectiveTransform(pts1,pts2)
	imgOutput = cv2.warpPerspective(img,matrix,(width,height))
	
	# cropping/rotation method two - imutils four point transform
	# ~ pts1 = np.array([corners[0][0],corners[6][0],corners[42][0],corners[48][0]])
	# ~ imgOutput = perspective.four_point_transform(img, pts1)
	# ~ resized = cv2.resize(imsgOutput, dim, interpolation = cv2.INTER_AREA)
	
	# output
	return imgOutput

def detectRectI(img):
	"""Warps perspective to crop picture to chess board.
	img = the picture you want to crop
    returns the crppped image that is just the chess board
    """
	chessboardSize = (7,7)
	frameSize = (330,640)
	
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	# Find the chess board corners
	ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)
	
	# output image size
	width, height = 512,512
	dim = (width, height)
	
	# get corners using inside points and a pixel offset
	offset = 25
	corners[0] = [corners[0][0][0]-offset,corners[0][0][1]-offset]
	corners[6] = [corners[6][0][0]+offset,corners[6][0][1]-offset]
	corners[42] = [corners[42][0][0]-offset,corners[42][0][1]+offset]
	corners[48] = [corners[48][0][0]+offset,corners[48][0][1]+offset]
	
	# cropping/rotation method one - opencv warp perspective
	pts1 = np.array([corners[0],corners[6],corners[42],corners[48]])
	pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
	matrix = cv2.getPerspectiveTransform(pts1,pts2)
	imgOutput = cv2.warpPerspective(img,matrix,(width,height))
	
	# cropping/rotation method two - imutils four point transform
	# ~ pts1 = np.array([corners[0][0],corners[6][0],corners[42][0],corners[48][0]])
	# ~ imgOutput = perspective.four_point_transform(img, pts1)
	# ~ resized = cv2.resize(imsgOutput, dim, interpolation = cv2.INTER_AREA)
	
	# output
	return imgOutput