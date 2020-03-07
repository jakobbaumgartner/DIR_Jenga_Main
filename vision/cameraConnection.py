import numpy as np
import cv2
import time
# import imutils

import vision.recognizer as recognizer

def startCameras(q, flag = 'normal'):

    cam1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.waitKey(1)
    cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cam1.set(cv2.CAP_PROP_FOCUS, 30) # set focus 0-255, increments of 5
    cam1.set(cv2.CAP_PROP_SATURATION, 250)
    

    cam2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cv2.waitKey(1)
    cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
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

            if(flag == 'testing'):

                # nice visualization, too processor consuming for normal operation
               
                coordinates1 = recognizer.getDots(frame1,'mask1', np.array([20, 100, 0]), np.array([40, 255, 255]), 60, 255)
                coordinates2 = recognizer.getDots(frame2,'mask2', np.array([20, 100, 0]), np.array([40, 255, 255]), 60, 255)

                recognizer.printImages(frame1, 'dots1' ,coordinates1)
                recognizer.printImages(frame2, 'dots2' ,coordinates2)
                time.sleep(1)



            q.put([cam1.isOpened(), frame1, frame2, cam2.isOpened()])
            # print('thread running')
    
    
    print('camera error')


# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html	# VideoCapture Settings:
# https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html



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