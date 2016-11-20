def tupleToList(point):
    return [point[0], point[1]]

def listToTuple(point):
    return (point[0], point[1])

def averagePoint(pointA,pointB):
    x = (pointA[0] + pointB[0]) /2
    y = (pointA[1] + pointB[1]) / 2
    return [x,y]

def obtainCenterOfHand(triangles):
    center = [0, 0]
    for triangle in triangles:
        center[0] += triangle.defect[0]
        center[1] += triangle.defect[1]
    center[0] /= len(triangles)
    center[1] /= len(triangles)
    return center

class Triangle:
    fingerA = []
    fingerB = []
    defect = []

    def __init__(self, fingerA, fingerB, defect):
        self.fingerA = tupleToList(fingerA)
        self.fingerB = tupleToList(fingerB)
        self.defect = tupleToList(defect)