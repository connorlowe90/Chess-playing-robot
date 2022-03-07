import cv2
import numpy as np
from skimage import data,io,filters
from skimage.measure import compare_ssim as ssim
from boardNotation import *
from stockfish import Stockfish
from os import *
sys.path.insert(1, '//home/pi/ee475')
from imgUtils.boardNotation import *

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
	
# get indices of 4 minimum return none if castling has not occured
def find4Mins(imgA, imgB, imgBlank, tune = 0.6):	
	ssimArray = getSSIM(imgA, imgB, imgBlank)
	A, B, C, D = np.partition(ssimArray, 3)[0:4]  # k=1, so the first two are the smallest items
	
	index1 = np.where(ssimArray == A)[0][0]
	index2 = np.where(ssimArray == B)[0][0]
	index3 = np.where(ssimArray == C)[0][0]
	index4 = np.where(ssimArray == D)[0][0]
	print(index1, index2, index3, index4)
	
	out2 = []
	out2.append(str(index1))
	out2.append(str(index2))
	out2.append(str(index3))
	out2.append(str(index4))
	if (A < tune and B < tune and C < tune and D < tune):
		return index1, index2, index3, index4, out2
	else:
		return None, None, None, None, None
		
def getSSIM(imgA, imgB, imgBlank):
	# window slide and save 64 images X 2 (before and after)
	imgASlide, imgBSlide = getImgSlide(imgA, imgB)
	imgA2Slide, imgBlankSlide = getImgSlide(imgA, imgBlank)  

	# analyze slide	
	return analyzeSlide(imgASlide, imgBSlide)
	
