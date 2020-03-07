import numpy as np
import cv2
# import imutils


def startCameras(q):

    cam1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.waitKey(1)
    cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cam1.set(cv2.CAP_PROP_FOCUS, 30) # set focus 0-255, increments of 5
    cam1.set(cv2.CAP_PROP_SATURATION, 250)
    

    cam2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cv2.waitKey(1)
    cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cam2.set(cv2.CAP_PROP_FOCUS, 30) # set focus 0-255, increments of 5
    cam2.set(cv2.CAP_PROP_SATURATION, 250)

    cv2.namedWindow('Camera1', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Camera2', cv2.WINDOW_NORMAL)

    if not(cam1.isOpened() == False or cam2.isOpened() == False): 
       
        
        while 1:
        
            ret1, frame1 = cam1.read()
            ret2, frame2 = cam2.read()
            cv2.imshow('Camera1', frame1)
            cv2.waitKey(1)
            cv2.imshow('Camera2', frame2)
            cv2.waitKey(1)

            q.put([cam1.isOpened(), frame1, frame2, cam2.isOpened()])
            # print('thread running')
    
    
    print('camera error')


