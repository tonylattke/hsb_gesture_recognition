# HSB - Computational Geometry
# Professor: Martin Hering-Bertram
# Authors:  Filips Mindelis
#           Tony Lattke

# Python Libraries
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
