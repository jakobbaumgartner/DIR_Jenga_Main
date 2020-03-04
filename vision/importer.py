import numpy as np
import cv2
import imutils

class importer:

	def getImage(open):

		# different source imports
		
		if open == 'file':
			image = cv2.imread('./kamera_m0/b1.jpg')
			source = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		if open == 'camera0':
			cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		


			cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
			cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

			cap.set(cv2.CAP_PROP_FOCUS, 30) # set focus 0-255, increments of 5
			cap.set(cv2.CAP_PROP_SATURATION, 250)

			ret, frame = cap.read()

			# rotation of image
			frame = imutils.rotate_bound(frame, -90)

			source = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			cap.release()
			image = frame

		if open == 'camera1':
			cap = cv2.VideoCapture(1)
			ret, frame = cap.read()
			source = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			cap.release()
			image = frame

		# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
		# VideoCapture Settings:
		# https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html

		return [image, source]

# 0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
# 1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
# 2. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
# 3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
# 4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
# 5. CV_CAP_PROP_FPS Frame rate.
# 6. CV_CAP_PROP_FOURCC 4-character code of codec.
# 7. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
# 8. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
# 9. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
# 10. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
# 11. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
# 12. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
# 13. CV_CAP_PROP_HUE Hue of the image (only for cameras).
# 14. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
# 15. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
# 16. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
# 17. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
# 18. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)
# 28. CV_CAP_PROP_FOCUS focus