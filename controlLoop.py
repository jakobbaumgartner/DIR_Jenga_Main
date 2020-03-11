#code files

import settingsFile                                     # FIX THIS, IT SHOULD BE JSON FILE!!!!
import yumi.yumiConnection as yumiConnection
import vision.cameraConnection as cameraConnection
import vision.recognizer as recognizer

# dependencies
import numpy as np
import cv2
import threading
import queue
import time
import socket
# import imutils

# shared memory for threads
q = queue.Queue()


setInput = 'not set'
socketStatus = 'unknown'
sensorStatus = 'unknown'
cameraStatus = 'unknown'
buttonStatus = 'unknown'

# Start all modules here:




    # ---------------------------------------------------------------------------------------
    # Start Camera:

camera = threading.Thread(target=cameraConnection.startCameras, args=(q,'testing'), daemon=True)

camera.start()
camstatus1 = q.get()[0]
camstatus2 = q.get()[3]
cameraImage1 =q.get()[1]  # to get image from camera1
cameraImage2 = q.get()[2]   # to get image from camera2
cameraStatus = '  ' + str(camstatus1)+ '  ' + str(camstatus2)

if (camstatus1 == False or camstatus2  == False): 
    cameraStatus  += '   ERROR!'


    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # Start Yumi Connection:

# yumi = yumiConnection.startSocket(settingsFile.yumi_IP, settingsFile.yumi_port)  -->      WHEN CONNECTED TURN OFF!
# socketStatus = settingsFile.yumi_IP + ', ' + str(settingsFile.yumi_port)

socketStatus = 'Turned off.'
    # ---------------------------------------------------------------------------------------


    # ---------------------------------------------------------------------------------------
    # Start Arduino

                # TO ADD.

    # ---------------------------------------------------------------------------------------

    



print('\n \n----------------------------------------------------------')

print(' YENGA v 0.1')
print('\nProgram initiated:')
print('Socket status: ' + str(socketStatus))
print('Sensor status: ' + str(sensorStatus))
print('Camera status: ' + str(cameraStatus))
print('Button status: ' + str(buttonStatus))

print('----------------------------------------------------------\n')





setInput = input('Please set input: ')

while ( setInput != 'exit'):

    if (setInput == 'pvg'):
        
        # This is player vs game. Computer makes a move, then players makes a move and presses button and so on, until someone wins.
        

        print('\n----------------------------------------------------------')
        print('----------------------------------------------------------\n')
        print('\nWelcome to player - vs - game !')
        print('\nPlease wait for computer to make a move, after that you make a move and when finished press the button to let computer know it is its time again.\n')

        while ( setInput != 'exit' and setInput != 'end'):
            
            # This is the actual program loop, it will keep running until the game is finished.
            print('loop')
            

            # TO ADD.





    if (setInput == 'pvp'):

        # This is a player vs player mode, with a twist. Players take turns in choosing which block robot pulls out.

        print('\n----------------------------------------------------------')
        print('----------------------------------------------------------\n')
        print('\nWelcome to player - vs - player !')
        print('\nThis is a player vs player mode, with a twist. Players take turns in choosing which block robot pulls out.\n')
        
 
        

    setInput = input('\nPlease set input: ')


