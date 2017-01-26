# HSB - Computational Geometry
# Professor: Martin Hering-Bertram
# Authors:  Filips Mindelis
#           Tony Lattke

from numpy import sqrt, arccos, rad2deg

class TriangleN:
    cent = []
    rect1 = []
    rect2 = []

    # Contructor
    def __init__(self, cent, rect1, rect2):
        self.cent = cent
        self.rect1 = rect1
        self.rect2 = rect2

    # Calculates the angle between two lines
    def angle(self):
        v1 = (self.rect1[0] - self.cent[0], self.rect1[1] - self.cent[1])
        v2 = (self.rect2[0] - self.cent[0], self.rect2[1] - self.cent[1])
        dist = lambda a:sqrt(a[0] ** 2 + a[1] ** 2)
        angle = arccos((sum(map(lambda a, b:a*b, v1, v2))) / (dist(v1) * dist(v2)))
        angle = abs(rad2deg(angle))
        return angle

# def averagePoint(pointA, pointB):
#     x = (pointA[0] + pointB[0]) / 2
#     y = (pointA[1] + pointB[1]) / 2
#     return [x, y]


# def obtainCenterOfHand(triangles):
#     center = [0, 0]
#     for triangle in triangles:
#         center[0] += triangle.defect[0]
#         center[1] += triangle.defect[1]
#     if len(triangles) > 0:
#         center[0] /= len(triangles)
#         center[1] /= len(triangles)
#     else:
#         center = [-1,-1]
#     return center
