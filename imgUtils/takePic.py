import cv2

# takes a picture using cv2 and returns the frame
def takePic():
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
	ret, frame = cap.read()
	return frame


