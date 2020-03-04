import numpy as np
import cv2
# import imutils

def startCamera(camera_id):

    cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)



    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    cap.set(cv2.CAP_PROP_FOCUS, 30) # set focus 0-255, increments of 5
    cap.set(cv2.CAP_PROP_SATURATION, 250)

    return cap