from favourites import favourites

def addWeightoCoordinates (coordinates):
    # function adds third field to coorinates list

    coordinatesWithWeights = []

    for element in coordinates:
        element.append(100)
        coordinatesWithWeights.append(element)
        print(element)

    return coordinatesWithWeights


def setWeights (coordinatesWithWeights, otherSide, bottom, block):
    #function sets order of pushes according to weights

    # weights:

    weight_level_top = 25/2
    weight_massPointDisplacementFromMid = 25/2
    weight_levels_above_single_bool = 10
    weight_levels_above_single_many = 10

    # other variables:

    unstableTopLevels = 10

    for block in coordinatesWithWeights:

        # UNSTABLE TOP LEVELS
        # if the block is in top some levels it will loose points, twice as much is if is even closer to the top
        if (((level_top(favourites, coordinatesWithWeights, block))-unstableTopLevels) < 0):
            block[3] -= weight_level_top

        if (((level_top(favourites, coordinatesWithWeights, block))-unstableTopLevels/2) < 0):
            block[3] -= weight_level_top

        # MASS POINT
        # if the block is mid, there is no lost points, because it is likely good candidate, if it is left or right there are lost points

        if ( block[0] == 0):
            # if block is on left side
            block[3] += favourites.massPointDisplacementFromMid(favourites, coordinatesWithWeights, block)*weight_massPointDisplacementFromMid

        if ( block[0] == 2):
            # if block is on right side
            block[3] -= favourites.massPointDisplacementFromMid(favourites, coordinatesWithWeights, block)*weight_massPointDisplacementFromMid


        # SINGLE LEVELS

        # ( All the single levels (All the single levels)
        # All the single levels (All the single levels)
        # All the single levels
        # Now put your hands up )

        if ( levels_above_single(favourites, bottomlevelside, risedlevelside, bottom, block)[1] ):
            # if there is a single level somewhere under, immediately loose 10 points
            block[3] -= weight_levels_above_single_bool

            # loose even more points, for one or more singles

            block[3] -= levels_above_single(favourites, bottomlevelside, risedlevelside, bottom, block)[3]*weight_levels_above_single_many + levels_above_single(favourites, bottomlevelside, risedlevelside, bottom, block)[4]*weight_levels_above_single_many


        # REMOVES BOTTOM LEVEL FROM PUSHING 

        if ( bottom == True and block[2] == 0):
            block[3] -= 100

    return coordinatesWithWeights

        
        
        




