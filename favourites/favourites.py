class favourites:

	def numberOfBlocksAbove(self,array, block):

		# checks how many blocks are in each of columns above the line
		
		elementsAbove = []
		# 1. remove all lines but those above 

		for element in array:
			if (element[1] > block[1]):
				elementsAbove.append(element)

		# 2. loop thrue remaining elements and count 
		LMR = [0, 0, 0]

		for element in elementsAbove:
			if(element[0] == 0):
				LMR[0] += 1

			if(element[0] == 1):
				LMR[1] += 1

			if(element[0] == 1):
				LMR[2] += 1
			
		# 3. return [L, M, R]
		print(' -------------------------- ')
		print('numberOfBlocksAbove: ' + str(LMR))

		return LMR

	def massPointDisplacementFromMid (self, array, block):

		# tells how is mass arranged from middle block or center of row

		LMR = self.numberOfBlocksAbove(self, array, block)

		# Get number of blocks left and right columns.
		# Get different number ob blocks in columns, divided by total number of blocks in side columns.

		displacement = (LMR[2]-LMR[0])/(LMR[0]+LMR[2])
		print(' -------------------------- ')
		print('massPointDisplacementFromMid: ' + str(displacement))
		
		return displacement


	def massPointDisplacementFromBlock (self, array, block):

		 # tells how is mass arranged from  block itself,
		#  !!! implementation is kind of lacking !!! 

		LMR = self.numberOfBlocksAbove(self, array, block)
		# factor is based on different effect of distance from column
		factor = 1

		if( block[0] == 0):
			displacement = (LMR[1]*factor + LMR[2]) / (LMR[0]+ LMR[1]*factor + LMR[2])         

		if( block[0] == 1):
			displacement = self.massPointDisplacementFromMid(self, array, block)
		
		if( block[0] == 2):
			 displacement = -(LMR[1]*factor + LMR[0]) / (LMR[0]+ LMR[1]*factor + LMR[2])

		print(' -------------------------- ')
		print('massPointDisplacementFromBlock: ' + str(displacement))
		

		return displacement

	def block_level (self, array, block):
		# Returns position of block in line and other two blocks in following format:
		# ['L', [1,0,1]]

		# check what is the first number of block
		LMR = '0'

		if block[0] == 0:
			LMR = 'L'
		
		if block[0] == 1:
			LMR = 'M'
		
		if block[0] == 2:
			LMR = 'R'

		line = []

		for x in array:
			if (x[1] == block[1]):
				line.append(x)

		# go one by one and create array

		arrayLine = [0,0,0]

		for x in line:
			if (x[0] == 0):
				arrayLine[0] = 1
			if (x[0] == 1):
				arrayLine[1] = 1
			if (x[0] == 2 ):
				arrayLine[2] = 1
		print(' -------------------------- ')
		print('block_level:  ' + str([LMR, arrayLine]))

		return [LMR, arrayLine]


	def level_bottom (self, block, array):
		return block[1]

	
	def level_top(self, array, block):
		# returns how many blocks from the top is current block

		max_level = 0

		for x in array:
			if(x[1] > max_level):
				max_level = x[1]
		
		print(' -------------------------- ')
		print('Max level:  ' + str(max_level-block[1]))
		
		return (max_level-block[1])


	def levels_above_single(self, bottomlevelside, risedlevelside, bottomblock, block):
		# returns how many level above first single level are we

		# bottomlevelside is the side of yenga, which of which is the first level laying directly
		# on the support or ground, risedlevelside is the other one

		# bottomblock checks if our block is on the side that lays on the ground or the other one
		# if it is the other one, we need to look on the other side different for one level

		levels_under_bottomlevelside = []
		levels_under_risedlevelside = []

		single_under_bottomlevel = []
		single_under_risedlevel = []

		#we only keep levels under the one we are looking at

		if (bottomblock):	
			for element in bottomlevelside:
				if ( block[1] > element[1]):
					levels_under_bottomlevelside.append(element)

			for element in risedlevelside:
				if ( block[1] > element[1]):
					levels_under_risedlevelside.append(element)
		
		else:
			# if we are looking from side that is not on ground we need to count one level more for other side
			for element in bottomlevelside:
				if ( block[1]+1 > element[1]):
					levels_under_bottomlevelside.append(element)

			for element in risedlevelside:
				if ( block[1] > element[1]):
					levels_under_risedlevelside.append(element)


		for element in levels_under_bottomlevelside:
			if ( (self.block_level(self, bottomlevelside, element))[1] == [0,1,0] ):
				single_under_bottomlevel.append(element[1])

		for element in levels_under_risedlevelside:
			if ( (self.block_level(self, risedlevelside, element))[1] == [0,1,0] ):
				single_under_risedlevel.append(element[1])

		single_under_bottomlevel.sort()
		single_under_risedlevel.sort()

		firstsingulbottomside = single_under_bottomlevel[0]
		firstsingulrisedlevel = single_under_risedlevel[0]

		# see if there are single levels

		if ( len(single_under_bottomlevel) + len(single_under_risedlevel) > 0):
			single = True
		else:
			single = False


		# return data about single level on same side and on the other side,
		# return if any, how far from first one, how many, and list of all

		if (bottomblock): 
			return [single, firstsingulbottomside, firstsingulrisedlevel, len(single_under_bottomlevel), len(single_under_risedlevel), single_under_bottomlevel, single_under_risedlevel]
		
		else:
			return [single, firstsingulrisedlevel, firstsingulbottomside, len(single_under_risedlevel), len(single_under_bottomlevel), single_under_risedlevel, single_under_bottomlevel]

		# levels_above_single IS UNTESTED !!!!!!!!!!!!!!!!!!!!!1 WARNING






