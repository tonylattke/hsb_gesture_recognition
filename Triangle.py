# HSB - Computational Geometry
# Professor: Martin Hering-Bertram
# Authors:  Filips Mindelis
#           Tony Lattke

# Tuple to List
def tupleToList(point):
    return [point[0], point[1]]


# List to tuple
def listToTuple(point):
    if point is not None:
        return (point[0], point[1])
    else:
        return (0, 0)


# Calculates the average between pointA and pointB
def averagePoint(pointA, pointB):
    x = (pointA[0] + pointB[0]) / 2
    y = (pointA[1] + pointB[1]) / 2
    return [x, y]


# Calculates the center of the Hand
def obtainCenterOfHand(triangles):
    center = [0, 0]
    for triangle in triangles:
        center[0] += triangle.defect[0]
        center[1] += triangle.defect[1]
    if len(triangles) > 0:
        center[0] /= len(triangles)
        center[1] /= len(triangles)
    else:
        center = [-1, -1]
    return center


class Triangle:
    fingerA = []
    fingerB = []
    defect = []

    def __init__(self, fingerA, fingerB, defect):
        self.fingerA = tupleToList(fingerA)
        self.fingerB = tupleToList(fingerB)
        self.defect = tupleToList(defect)
