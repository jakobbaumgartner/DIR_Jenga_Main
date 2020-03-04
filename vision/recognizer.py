import numpy as np
import cv2

class recognizer:
	
	def getDots (source, low, high, treshold, max_treshold):
		
		# source is HSV file 

		# low and high are settings for green levels in numpy format, look example:
		# low_filter = np.array([40, 100, 0])
		# high_filter = np.array([190, 255, 255])

		# treshold and max_treshold are settings for contour

		# set color filter and run it on the image
		mask = cv2.inRange(source, low, high)
		#filter out dots with mask
		dots = cv2.bitwise_and(source, source, mask=mask) 

		# convert from HSV to RGB, than to GRAY and use blurring 
		dotsRGB = cv2.cvtColor(dots, cv2.COLOR_HSV2RGB)
		dotsGray = cv2.cvtColor(dotsRGB, cv2.COLOR_RGB2GRAY)
		dotsGraybl = cv2.blur(dotsGray, (5,5))

		# using tresholding convert form GRAY to B&W
		retval, dotsBW = cv2.threshold(dotsGraybl, treshold, max_treshold,	cv2.THRESH_BINARY) 

		# contour returns just a couple of points for every 'dot'
		cnts = cv2.findContours(dotsBW.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		cv2.namedWindow('dots', cv2.WINDOW_NORMAL)
		cv2.imshow('dots', dotsRGB)
		# for every point out of contour get coordinates and calculate an average of x and y. That is the center of
		# our dots. The dots are kind of 'circular', so it should be quite accurate.
		coordinates = []
		# dotsRGBc = dotsRGB

		for element in cnts[0]:
			count = 0
			x = 0
			y = 0

			for tocka in (element):
				count+=1

				x = x + tocka[0][0]
				y= y + tocka[0][1]

				
			coordinates.append([int(x/count), int(y/count)])

		print('\n-------------------------------------------------------')
		print('\n  List of coordinates: \n')
		print(coordinates)

		return coordinates

	def simpleArray (array, width, maxRowOffset):

		# get borders for columns
		columnBorder1 = width/3
		columnBorder2 = width*2/3

		column0 = []
		column1 = []
		column2 = []
		rows = []

		# sort all point

		for element in array:
			if (element[0] <= columnBorder1):
				column0.append(element[1])
			if (element[0] > columnBorder1 and element[0] <= columnBorder2):
				column1.append(element[1])
			if (element[0] > columnBorder2):
				column2.append(element[1])
		# print(width)
		# print(" -- Column 0: -- ")
		# print(column0)
		# print(" -- Column 1: -- ")
		# print(column1)
		# print(" -- Column 2: -- ")
		# print(column2)




		# set rows looking at first column
		for element in column0: 
			exists = False

			for row in rows:
				if abs(element-row) < maxRowOffset:
					exists = True

			if exists == False:
				rows.append(element)

		
		# set rows looking at second column
		for element in column1: 
					exists = False

					for row in rows:
						if abs(element-row) < maxRowOffset:
							exists = True

					if exists == False:
						rows.append(element)

		
		# set rows looking at third column
		for element in column2: 
					exists = False

					for row in rows:
						if abs(element-row) < maxRowOffset:
							exists = True

					if exists == False:
						rows.append(element)


		rows.sort()
		print(" -- Rows: -- ")
		print(rows)



		# create points in columns and rows

		simpleArrayReturn = []
		# set rows looking at first column
	
		for element in column0: 
			
			for num, row in enumerate(rows, start=0):

				if(abs(row-element) < maxRowOffset):
					simpleArrayReturn.append([0, len(rows)-num])
		
		# set rows looking at second column
		for element in column1: 
				
					for num, row in enumerate(rows, start=0):

						if(abs(row-element) < maxRowOffset):
							simpleArrayReturn.append([1, len(rows)-num])

						
		
		# set rows looking at third column
		for element in column2: 
					
					for num, row in enumerate(rows, start=0):
						
						if(abs(row-element) < maxRowOffset):
							simpleArrayReturn.append([2, len(rows)-num])

		# create simple tower representation:
		simpleTower = []
		
		x = 0
		while x < (3*len(rows)):
			simpleTower.append(0)
			x+=1


		for x in simpleArrayReturn:
			simpleTower[x[1]*3-3+x[0]] = 1

		print(" --- ")
		for num, block in enumerate(simpleTower, start=0):   
			print(block, end='  ')
			

			if ((num+1) % 3 == 0):
				print ("- ", end='')

		print('\n \n')
		print(simpleArrayReturn)
		print('\n \n')
		print(simpleTower)




		

