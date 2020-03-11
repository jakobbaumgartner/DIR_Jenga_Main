import numpy as np
import cv2

from favourites import favourites
import favouritesConnection


array = [[0, 1], [0, 2], [0, 3], [0, 5], [0, 6], [1, 1], [1, 2], [1, 4], [1, 5], [1, 7], [2, 1], [2, 3], [2, 5], [2, 6]]
# favourites.level_top(favourites, array, [0, 2] )

print(favouritesConnection.addWeightoCoordinates(array))

