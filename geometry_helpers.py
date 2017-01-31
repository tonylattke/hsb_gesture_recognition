# HSB - Computational Geometry
# Professor: Martin Hering-Bertram
# Authors:  Filips Mindelis
#           Tony Lattke

# Geometry Helpers

# Python Libraries
import math  # Math operations


# Calculates the distance between points
def distance(pointA, pointB):
    return math.sqrt((pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2)


# Calculates the angle between 3 Points
def calculateAngle(start, end, far):
    a = distance(start, end)
    b = distance(far, start)
    c = distance(end, far)
    return math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 60


# Calculates the mirror for pointA and pointB
def mirrorPoint(pointA, pointB):
    deltaX = math.fabs(pointB[0] - pointA[0])
    deltaY = math.fabs(pointB[1] - pointA[1])
    ab = distance(pointA, pointB)
    k = ab * math.sqrt(1 / (deltaX ** 2 + deltaY ** 2))
    x = pointA[0] + deltaX * k
    y = pointA[1] + deltaY * k
    return [int(x), int(y)]


# Calculates the center of a list of points
def obtainCenterOfPoints(points):
    center = [0, 0]
    for point in points:
        center[0] += point[0]
        center[1] += point[1]
    if len(points) > 0:
        center[0] /= len(points)
        center[1] /= len(points)
    else:
        center = [-1, -1]
    return center
