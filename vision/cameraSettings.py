import numpy as np
import cv2
import json

class cameraSettings:

    areaPointsX = []
    areaPointY = 0
    wait = True
    

    def getPoint(self, image):

        # To get X coordinates click twice left mouse button, to get Y click once right mouse button, 
        # to clear values click middle mouse button. To save values press altkey and move mouse just a bit.

        # open image
        cv2.namedWindow('settings', cv2.WINDOW_NORMAL)
        cv2.imshow('settings', image)
        # get two clicks and save coordinates

        cv2.setMouseCallback('settings', self().getCoordinate, param = None)
      
        self.image = image
        self.source = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
     



    def getCoordinate(self, event, x, y, flag, other):
        # print(str(x) + ' - ' + str(y))
        

        if(flag == 1):
            if(len(self.areaPointsX) < 2):
                print('-----------')
                self.areaPointsX.append(x)
                print(self.areaPointsX)
                print('-----------')
                print(self.source[y, x])
            else:
                print('ERROR - TOO MANY POINTS.')

        if(flag == 2):
            print('-----------')
            self.areaPointY = y
            print(self.areaPointY)
            print('-----------')

        if(flag == 4):
            # delete all values
            self.areaPointsX = []
            self.areaPointY = 0
            print('VALUES CLEARED, INPUT AGAIN.')
            return 0
        
        if (flag == cv2.EVENT_FLAG_ALTKEY):
            cv2.destroyWindow("settings")
            data = {
                "x1": self.areaPointsX[0],
                "x2": self.areaPointsX[1],
                "y": self.areaPointY
            }
            jdata = json.dumps(data)
            print(jdata)
            with open('./Settings/cameraCutSettings.json', 'w') as outfile:
                json.dump(data, outfile)

            with open('./Settings/cameraCutSettings.json') as datafile:
                data = json.load(datafile)
            cv2.namedWindow('cut', cv2.WINDOW_NORMAL)
            # cv2.resizeWindow('cut', 600,600)

            cv2.imshow('cut', self.image[0:data['y'], data['x1']:data['x2']])
            print('WINDOW CLOSED')
        
        
    def getCut(self, image):

        # Function returns part of image based on input coordinates.

        with open('./Settings/cameraCutSettings.json') as datafile:
            data = json.load(datafile)

        print(data)
        
        return image[data['x1']:data['x2'], 0:data['y']]
