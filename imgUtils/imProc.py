import cv2
import numpy as np
from skimage import data,io,filters
from skimage.measure import compare_ssim as ssim
from boardNotation import *
from stockfish import Stockfish
from os import *

# engine using stockfish package
stockfish = Stockfish('/home/pi/ee475/Chess-Engines-for-Raspberry-Pi-by-Al-master/arm7l/t-fruit')

# breaks 2 images into 2 different 64 image arrays for each square, sized 64pixelsx64pixels
def getImgSlide(imgA, imgB):
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
	return imgASlide, imgBSlide

# analyzes structrual similarity index of pictures 
def analyzeSlide(imgASlide, imgBSlide):
	ssimArray = np.zeros(64)
	for i in range(0, 64):
		ssimArray[i] = ssim(imgBSlide[i], imgASlide[i], multichannel=True)
	return ssimArray

# get indices of 2 minimum	
def find2Mins(ssimArray):	
	A, B = np.partition(ssimArray, 1)[0:2]  # k=1, so the first two are the smallest items
	index1 = np.where(ssimArray == A)[0][0]
	index2 = np.where(ssimArray == B)[0][0]
	return index1, index2
	
# gets user move from 2 images
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
