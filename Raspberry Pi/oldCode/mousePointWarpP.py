# imports
import cv2
import numpy as np

# to store mouse clicks
circles = np.zeros((4,2),int)
counter = 0

# callback function to track mouse clicks
def mousePoints(event,x,y,flags,params):
	global counter
	if event == cv2.EVENT_LBUTTONDOWN:
		circles[counter] = x,y
		counter = counter + 1

# Using cv2.imread() method
img = cv2.imread('test.bmp')

# output image size
width, height = 512,512

# warp perspective
while counter < 5:
	if counter == 4:
		pts1 = np.float32([circles[0],circles[1],circles[2],circles[3]])
		pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
		matrix = cv2.getPerspectiveTransform(pts1,pts2)
		imgOutput = cv2.warpPerspective(img,matrix,(width,height))
		cv2.imshow("output", imgOutput)
		
		# force return
		counter = counter + 1

	# image to take points from
	cv2.imshow("original", img)
	cv2.setMouseCallback("original", mousePoints)
	cv2.waitKey(1)
