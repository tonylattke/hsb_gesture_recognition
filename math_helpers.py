# HSB - Computational Geometry
# Professor: Martin Hering-Bertram
# Authors:  Filips Mindelis
#           Tony Lattke

# Python Libraries
from numpy import sqrt


# Calculates the distance between points
def distance(pointA, pointB):
    return sqrt((pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2)


# Tuple structure to List
def tupleToList(point):
    return [point[0], point[1]]


# List to Tuple structure
def listToTuple(point):
    if point is not None:
        return (point[0], point[1])
    else:
        return (0, 0)


# smoothPositionY - Generate a smooth value of y
# x - X coordinate
# y - Y coordinate
# n - Smooth factor
def smoothPositionY(x, y, n):
    return (y / x) * n


# Radious settings
radious = {
    'finger': {
        'intern': 10,
        'extern': 5,
    },
    'defect': {
        'intern': 10,
        'extern': 5,
    },
    'centerOfHand': {
        'intern': 20,
        'extern': 10,
    }
}
