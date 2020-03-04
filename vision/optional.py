import numpy as np
import cv2

class optional:
	def printImages(image, dots):
		# image is source photo, dots are coordinates of points in array

		for i in dots:
			cv2.circle(image, (i[0], i[1]), 10, (0, 0, 255), 1)


		cv2.namedWindow('source', cv2.WINDOW_NORMAL)
		cv2.imshow('source',image)

	def testfunction ():
		print('testfunction succesfull!!!')