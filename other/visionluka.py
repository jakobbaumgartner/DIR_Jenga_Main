import numpy as np
import cv2
import math
import pdb          #pdb.set_trace() #pol pa v konzolo našišeš "n" za naslednjo vrstico al pa "s" za naslednjo instrukcijo
import imutils
import time

import camera       #camera class with camera handlers (on openCV)
        
class XOvis:
    def __init__(self, width, height, cam_idx = 0, verbose = True, draw_debug = 2, divisor = 4):
        self.verbose = verbose
        self.draw_debug = draw_debug    #0-off | 1-only fancy things | 2-on
        self.draw_debug_p = -1  #previous draw debug, initially set to invalid number so that windows get updated
        self.divisor = divisor

        self.img_bgr = None
        self.img_hsv = None

        self.canvas_debug_scaler = 0.5
        self.canvas_w = 1600
        self.canvas_h = 1600
        self.calculate_canvas()

        exposure = -5
        colour_preset = 2
        if colour_preset == 0:  #daylight (in shadow)
            self.marker_bounds_g = [(85,90,80), (105,255,100)]
            self.marker_bounds_r = [(165, 100, 105), (175, 255, 255)]
            self.marker_bounds_x = [(100, 100, 80), (120, 255, 255)]
            exposure = -6
        elif colour_preset == 1:    #some daylight + indoor lights
            self.marker_bounds_g = [(85, 45, 60), (105, 255, 150)]
            self.marker_bounds_r = [(150, 110, 110), (175, 255, 255)]
            self.marker_bounds_x = [(0, 0, 0), (255, 255, 255)]
        elif colour_preset == 2:    #indoor lights
            self.marker_bounds_g = [(80, 45, 60), (95, 255, 150)]
            self.marker_bounds_r = [(160, 150, 140), (175, 255, 255)]
            #self.marker_bounds_x = [(80, 30, 0), (180, 255, 180)]
            self.marker_bounds_x = [(80, 30, 50), (180, 255, 180)]
        else:   #same as 0 (for now, to be changed)
            self.marker_bounds_g = [(75, 130, 60), (100, 255, 100)]
            self.marker_bounds_r = [(150, 130, 100), (175, 255, 255)]
            self.marker_bounds_x = [(0, 0, 0), (255, 255, 255)]

        self.c = camera.Camera(width, height, cam_idx = cam_idx, verbose = verbose, exposure = exposure)

        self.align_points = []     #high certainty alling points
        self.align_points_n = []   #low certainty alling points

    def calculate_canvas(self): # returns 2d numpy array (size sel.canvas_w x self.canvas_h)
        self.canvas = np.zeros((self.canvas_w, self.canvas_h,3), dtype="uint8")

    def find_markers(self): #find markers for alignment
        # masking for markers
        if True:    # erosion + dilation thingies
            kernel_size1 = (5,5)
            kernel_size2 = (3,3)
            # kernel = np.ones(kernel_size,np.uint8)
            kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size1)
            kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size2)

            masked_g = cv2.inRange(self.img_hsv, self.marker_bounds_g[0], self.marker_bounds_g[1])  # mask out markers based on HSV
            masked_r = cv2.inRange(self.img_hsv, self.marker_bounds_r[0], self.marker_bounds_r[1])  # mask out markers based on HSV

            filtered_g = cv2.morphologyEx(masked_g, cv2.MORPH_CLOSE, kernel1)   # dilate+erode
            filtered_g = cv2.erode(filtered_g, kernel2, iterations = 1)         # erode to eliminate spurious speckles
            filtered_r = cv2.morphologyEx(masked_r, cv2.MORPH_CLOSE, kernel1)   # same for red markers
            filtered_r = cv2.erode(filtered_r, kernel2, iterations=1)
        
        if False:   # marker detection results drawing (binary mask)
            cv2.namedWindow("Xg")
            cv2.namedWindow("Xr")
            cv2.imshow("Xg", filtered_g)
            cv2.imshow("Xr", filtered_r)
            #cv2.imshow("X", masked_g)#cv2.bitwise_and(self.img_bgr,self.img_bgr, mask = filtered_g))

        # get contours
        marker_contours_g, hierarchy_g = cv2.findContours(filtered_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        marker_contours_r, hierarchy_r = cv2.findContours(filtered_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # TBA: system for removing stray markers (based on previously confirmed markers)

        if True:    # checking for excess marker detections
            something_went_wrong = False    #for catching arrors at detecting too few or too many markers
            if len(marker_contours_g) != 1: #expecting exactly 1 green marker
                something_went_wrong = True
                if self.verbose:
                    print("detected ", len(marker_contours_g)," green markers instead of 1")
            if len(marker_contours_r) != 3: #expecting exactly 3 red markers
                something_went_wrong = True
                if self.verbose:
                    print("detected ", len(marker_contours_r), " red markers instead of 1")
            if something_went_wrong:
                return False

        if True:    # convert marker contours to points
            marker_contours = marker_contours_g + marker_contours_r #combine all 4 markers, green is the first one
            marker_centers = []
            for i in range(len(marker_contours)):   # go through all contours and find their centers
                try:
                    M = cv2.moments(marker_contours[i])
                    x = int(M["m10"]/M["m00"])
                    y = int(M["m01"]/M["m00"])
                    marker_centers.append([x,y])    #align points get stored as [Xcenter,Ycenter,Contour_idx] packets
                except ZeroDivisionError:
                    something_went_wrong = True
                    if self.verbose:
                        print("zero division error at calculating marker centers")
            if something_went_wrong:    #zero division messed things up
                return False

        # print centers
        if self.verbose:
            print("marker centers: ", marker_centers)
            #self.verbose = False    #short term workaround to only print it once

        # if all went well, arrange points in CW order (starting with green marker)
        failed, sorted = self.sort_align_points(marker_centers)
        if failed:
            something_went_wrong = True
            return False
        self.align_points = sorted

        

        return True

    def sort_align_points(self, points):
        # get the center of all 4 points
        x = sum([p[0] for p in points])/4
        y = sum([p[1] for p in points])/4

        # prepare vectors for further calculations
        vectors = [[p[0]-x,p[1]-y] for p in points]             # vectors from center of points to each point
        vectors = [[v[0]/math.hypot(v[0],v[1]), v[1]/math.hypot(v[0],v[1])] for v in vectors]    # for easier representation, can be commented out for actual use
        cross = [np.cross(vectors[0], v) for v in vectors[1:]]  # vector products between vector to 1st marker and others
        cross_abs = [abs(c) for c in cross]     # abs values of cross product
        #dot = [np.dot(vectors[0], v) for v in vectors[1:]]      # dot products between vector to 1st marker and others
        #print(points,list(np.around(vectors,2)), list(np.around(cross,2)), list(np.around(dot,2)))  # debug print; a bit fucky but it works

        # CW point has cross product approx 1, diagonal point has it around 0 and CCW point's is -1
        p1 = cross.index(max(cross))+1          # first CW point from green marker has cross product approximateli 1 (diagonal one's is 0), index has to be incremented by 1 because this vector skips 0th element
        p2 = cross_abs.index(min(cross_abs))+1  #index has to be incremented by 1 because this vector skips 0th element
        #p2 = dot.index(min(dot))+1              #this does the same thing previous line but requires more calculation to prepare list of dot products
        p3 = 6 - p1 - p2    # indexes can be 0,1,2 and 3; their sum is 6; first point is always at index 0 (I put it there); last point's index is derived thusly
        #print(len(points),p1,p2,p3)
        #print(points)
        try:
            output = [points[0], points[p1], points[p2], points[p3]]
        except IndexError:
            if self.verbose:
                print("error at aligning points (p1,p2,p3, pounts): ",p1,p2,p3,points)
            return True, False # something went wrong marker
        #print(output)
        return False, output

    def four_point_transform(self): #, image, pts):
        rect = np.array(self.align_points, dtype = "float32")

        
        # dst is generated the same way as self.canvas but omitting dst messes everything up
        dst = np.array([
            [0, 0],
            [self.canvas_w - 1, 0],
            [self.canvas_w - 1, self.canvas_h - 1],
            [0, self.canvas_h - 1]], dtype="float32")
    
        self.fpt = cv2.getPerspectiveTransform(rect, dst)       # compute transform (note that I had to use dst instead of self.canvas)
        self.canvas = cv2.warpPerspective(self.img_bgr, self.fpt, (self.canvas_w, self.canvas_h))   # apply the transform
        
        return True

    def analise_canvas(self): # finds contours of drawings and evaluates them
        # masking for markers
        if True:
            # erosion + dilation thingies
            kernel_size2 = (7, 7)
            kernel_size1 = (5, 5)
            kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size1)
            kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size2)

            canvas_hsv = cv2.cvtColor(self.canvas,cv2.COLOR_BGR2HSV)
            masked_x = cv2.inRange(canvas_hsv, self.marker_bounds_x[0], self.marker_bounds_x[1])  # mask out game based on HSV

            edge_mask = np.zeros((self.canvas_h, self.canvas_w), dtype="uint8")  # mask for cropping out edges of playing field
            edge_mask[19:self.canvas_h - 21, 19:self.canvas_w - 21] = 255  # 20px wide edges that will be cropped out
            masked_x = cv2.bitwise_and(edge_mask, masked_x)  # crop the field

            
            filtered_x = cv2.morphologyEx(masked_x, cv2.MORPH_CLOSE, kernel1)  # dilate+erode
            filtered_x = cv2.dilate(filtered_x, kernel2, iterations=1)  # erode to eliminate spurious speckles
            

        # marker detection results drawing (binary mask)
        if True:
            cv2.namedWindow("Xx")
            cv2.imshow("Xx", cv2.resize(filtered_x, (int(self.canvas_w * self.canvas_debug_scaler), int(self.canvas_h * self.canvas_debug_scaler))))

        #detecting contours
        #cnts = cv2.findContours(filtered_x, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnts, hierarchy = cv2.findContours(filtered_x, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)   # has two arrays - first one is array of contours and the second one is array of relations
        

        #handling contours
        colours = [(255,0,0),(255,128,0),(255,255,0),(128,255,0),(0,255,0),(0,255,128),(0,255,255),(0,128,255),(0,0,255),(128,0,255),(255,0,255),(255,0,128)]
        draw_debug_contours = True
        if True:
            valid_cnts = [] # list of indexes of valid contours
            cc = 5
            for (i, c) in enumerate(cnts):
                # compute the area of the contour along with the bounding box
                # to compute the aspect ratio
                (x, y, w, h) = cv2.boundingRect(c)
                #area = cv2.contourArea(c)
                hull_area = cv2.contourArea(cv2.convexHull(c))
                if hull_area < 1500:  # small speckles and stretched out lines should be ignored
                    continue
                valid_cnts.append(i)
            for i in range(len(valid_cnts)):
                c = cnts[valid_cnts[i]]
                area = cv2.contourArea(c)
                hull = cv2.convexHull(c)
                hullArea = cv2.contourArea(hull)
                solidity = area / (float(hullArea) + 1e-6)  #add something small to prevent zero division error
                simplified_hull = [cv2.approxPolyDP(hull,0.015*cv2.arcLength(hull,True),True)]

                if False and draw_debug_contours:   # draw contours
                    cv2.drawContours(self.canvas, c, -1, colours[cc%len(colours)], 2)
                    cv2.imshow("fpt", self.canvas)
                if True and draw_debug_contours:    # draw simplified convex hulls
                    cv2.drawContours(self.canvas, simplified_hull, -1, colours[cc%len(colours)], 2)
                #cv2.waitKey()
                cc += 1
                #==================================================================================================================================left off here
                # todo: hierarchy handling

    def tick(self):
        #do all the stuff/ call all the functions
        self.img_bgr = self.c.capture()
        self.img_hsv = cv2.cvtColor(self.img_bgr,cv2.COLOR_BGR2HSV)

        self.find_markers()
        if len(self.align_points) == 4:
            self.four_point_transform()
            self.analise_canvas()

        self.draw()
        return

    def draw(self):
        reset_windows_flag = False
        if self.draw_debug != self.draw_debug_p:
            self.draw_debug_p = self.draw_debug
            reset_windows_flag = True
            cv2.destroyAllWindows()
        
        debug_align_points = True   # draw numbers on markers
        if debug_align_points:
            if self.align_points:   # before markers are detected for the first time, array is empty 
                for i in range(4):
                    cv2.putText(self.img_bgr, str(i), tuple(self.align_points[i]), cv2.FONT_HERSHEY_COMPLEX, 0.5*self.divisor, (0, 0, 0), 2*self.divisor)
        
        if self.draw_debug == 0:
            return  #do nothing
        
        elif self.draw_debug == 1:
            #only fancy things
            if reset_windows_flag:  # prepare and position windows
                cv2.namedWindow("BGR")
                cv2.namedWindow("fpt")
                #cv2.namedWindow("T1")
            img_bgr_r = cv2.resize(self.img_bgr, (1920 // self.divisor, 1080 // self.divisor))
            cv2.imshow("BGR", img_bgr_r)
            if 1: #try:    # drawing canvas before it's ready seems to crash everything:/
                cv2.imshow("fpt", cv2.resize(self.canvas, (int(self.canvas_w * self.canvas_debug_scaler), int(self.canvas_h * self.canvas_debug_scaler))))
            else: #except:
                pass
            #amm = cv2.resize(self.align_marker_mask, (1920 // self.divisor, 1080 // self.divisor))
            #cv2.imshow("T1", amm)
            return
        
        else:
            #full draw defug
            if reset_windows_flag:      #prepare and position windows
                cv2.namedWindow("H")
                cv2.namedWindow("S")
                cv2.namedWindow("V")
                cv2.namedWindow("BGR")
                cv2.namedWindow("H11")
                cv2.namedWindow("R")
                cv2.namedWindow("G")
                cv2.namedWindow("B")
                cv2.namedWindow("T1")
                cv2.namedWindow("aligned")
                

                cv2.moveWindow("H",20,20)
                cv2.moveWindow("S",20,330)
                cv2.moveWindow("V",20,640)
                cv2.moveWindow("H11",510,20)
                cv2.moveWindow("BGR",510,330)
                cv2.moveWindow("R",1000,20)
                cv2.moveWindow("G",1000,330)
                cv2.moveWindow("B",1000,640)
                cv2.moveWindow("T1",510,640)


            img_bgr_r = cv2.resize(self.img_bgr,(1920//self.divisor,1080//self.divisor))  #resized version, for display
            img_hsv_r = cv2.resize(self.img_hsv,(1920//self.divisor,1080//self.divisor))
            cv2.imshow("H",img_hsv_r[...,0])
            cv2.imshow("S",img_hsv_r[...,1])
            cv2.imshow("V",img_hsv_r[...,2])
            cv2.imshow("BGR",img_bgr_r)
            cv2.imshow("R",img_bgr_r[...,2])
            cv2.imshow("G",img_bgr_r[...,1])
            cv2.imshow("B",img_bgr_r[...,0])

            img_h11 = img_hsv_r.copy()    #H11 = HSV with S and V values fixed
            img_h11[:,:,1]=128  #128 rather than 255 because that makes image much easier to look at
            img_h11[:,:,2]=128
            img_h11 = cv2.cvtColor(img_h11,cv2.COLOR_HSV2BGR)
            cv2.imshow("H11",img_h11)

            #amm = cv2.resize(self.align_marker_mask,(1920//self.divisor,1080//self.divisor))
            #cv2.imshow("T1", amm)

            try:
                cv2.imshow("aligned",self.img_alg)
            except AttributeError:
                if self.verbose:
                    print("cant display aligned image; not yet generated")

    def mouse_event(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x=x*self.divisor
            y=y*self.divisor
            print(x,y)
            print("BGR",self.img_bgr[y,x])
            print("HSV",self.img_hsv[y,x])
            print("")
        
if __name__ == "__main__":
    XOV = XOvis(1920,1080, verbose = False, divisor = 4, draw_debug=1)  #can use more settings, see class definition

    cv2.setMouseCallback("BGR", XOV.mouse_event)
    cv2.namedWindow("fpt")
    while 1:
        XOV.tick()
        cv2.setMouseCallback("BGR", XOV.mouse_event)

        tmp = cv2.waitKey(1) #0->1, da zajema konstantno
        if tmp == 27:
            break  # esc to quit
        else:
            XOV.c.kbd_event(tmp, True)
            
        continue
                       
    cv2.destroyAllWindows()