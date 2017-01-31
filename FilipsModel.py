# HSB - Computational Geometry
# Professor: Martin Hering-Bertram
# Authors:  Filips Mindelis
#           Tony Lattke

# Python Libraries
import cv2  # OpenCV

import Triangle as th
import geometry_helpers as gh


class FilipsModel:
    center = None
    center2 = None
    firstFinger = None
    firstDefect = None
    secondFinger = None
    secondDefect = None
    middleFinger = None
    defectMiddleFinger = None
    fourthFinger = None
    lastDefect = None
    lastFinger = None
    defects = 0

    def __init__(self, center, triangles):
        self.center = center
        self.defects = len(triangles)

        if self.defects == 0:
            pass
        elif self.defects == 1:
            self.firstFinger = triangles[0].fingerA
            self.firstDefect = triangles[0].defect
            self.lastFinger = triangles[0].fingerB
        elif self.defects == 2:
            self.firstFinger = triangles[0].fingerA
            self.firstDefect = triangles[0].defect
            self.secondFinger = th.averagePoint(triangles[0].fingerB, triangles[1].fingerA)
            self.lastDefect = triangles[1].defect
            self.lastFinger = triangles[1].fingerB
        elif self.defects == 3:
            self.firstFinger = triangles[0].fingerA
            self.firstDefect = triangles[0].defect
            self.secondFinger = th.averagePoint(triangles[0].fingerB, triangles[1].fingerA)
            self.secondDefect = triangles[1].defect
            self.middleFinger = th.averagePoint(triangles[1].fingerB, triangles[2].fingerA)
            self.lastDefect = triangles[2].defect
            self.lastFinger = triangles[2].fingerB
        elif self.defects == 4:
            self.firstFinger = triangles[0].fingerA
            self.firstDefect = triangles[0].defect
            self.secondFinger = th.averagePoint(triangles[0].fingerB, triangles[1].fingerA)
            self.secondDefect = triangles[1].defect
            self.middleFinger = th.averagePoint(triangles[1].fingerB, triangles[2].fingerA)
            self.defectMiddleFinger = triangles[2].defect
            self.fourthFinger = th.averagePoint(triangles[2].fingerB, triangles[3].fingerA)
            self.lastDefect = triangles[3].defect
            self.lastFinger = triangles[3].fingerB

    def drawLines(self, image, color, lineThickness):
        if self.defects == 0:
            pass
        elif self.defects == 1:  # 2 Fingers
            cv2.line(image, th.listToTuple(self.firstDefect), th.listToTuple(self.firstFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.firstDefect), th.listToTuple(self.lastFinger), color, lineThickness)
        elif self.defects == 2:  # 3 Fingers
            cv2.line(image, th.listToTuple(self.firstDefect), th.listToTuple(self.firstFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.firstDefect), th.listToTuple(self.secondFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.lastDefect), th.listToTuple(self.secondFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.lastDefect), th.listToTuple(self.lastFinger), color, lineThickness)
        elif self.defects == 3:  # 4 Fingers
            cv2.line(image, th.listToTuple(self.firstDefect), th.listToTuple(self.firstFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.firstDefect), th.listToTuple(self.secondFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.secondDefect), th.listToTuple(self.secondFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.secondDefect), th.listToTuple(self.middleFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.lastDefect), th.listToTuple(self.middleFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.lastDefect), th.listToTuple(self.lastFinger), color, lineThickness)
        elif self.defects == 4:  # 5 Fingers
            cv2.line(image, th.listToTuple(self.firstDefect), th.listToTuple(self.firstFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.firstDefect), th.listToTuple(self.secondFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.secondDefect), th.listToTuple(self.secondFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.secondDefect), th.listToTuple(self.middleFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.defectMiddleFinger), th.listToTuple(self.middleFinger), color,
                     lineThickness)
            cv2.line(image, th.listToTuple(self.defectMiddleFinger), th.listToTuple(self.fourthFinger), color,
                     lineThickness)
            cv2.line(image, th.listToTuple(self.lastDefect), th.listToTuple(self.fourthFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.lastDefect), th.listToTuple(self.lastFinger), color, lineThickness)

    def drawDefects(self, image, color, internRadius, externRadius):
        if self.defects == 0:
            cv2.circle(image, th.listToTuple(self.center), internRadius, color, externRadius)
        elif self.defects == 1:  # 2 Fingers
            cv2.circle(image, th.listToTuple(self.firstDefect), internRadius, color, externRadius)
        elif self.defects == 2:  # 3 Fingers
            cv2.circle(image, th.listToTuple(self.center), internRadius, color, externRadius)
            cv2.circle(image, th.listToTuple(self.firstDefect), internRadius, color, externRadius)
            cv2.circle(image, th.listToTuple(self.lastDefect), internRadius, color, externRadius)
        elif self.defects == 3:  # 4 Fingers
            cv2.circle(image, th.listToTuple(self.center), internRadius, color, externRadius)
            cv2.circle(image, th.listToTuple(self.firstDefect), internRadius, color, externRadius)
            cv2.circle(image, th.listToTuple(self.secondDefect), internRadius, color, externRadius)
            cv2.circle(image, th.listToTuple(self.lastDefect), internRadius, color, externRadius)
        elif self.defects == 4:  # 5 Fingers
            cv2.circle(image, th.listToTuple(self.center), internRadius, color, externRadius)
            cv2.circle(image, th.listToTuple(self.firstDefect), internRadius, color, externRadius)
            cv2.circle(image, th.listToTuple(self.secondDefect), internRadius, color, externRadius)
            cv2.circle(image, th.listToTuple(self.defectMiddleFinger), internRadius, color, externRadius)
            cv2.circle(image, th.listToTuple(self.lastDefect), internRadius, color, externRadius)

    def countOfFinger(self):
        if self.defects == 0:
            return 0
        return self.defects + 1

    def getCenter(self):
        if self.defects == 0:
            return [-1, -1]
        elif self.defects == 1:  # 2 Fingers
            centers = [self.firstFinger, self.lastFinger]
            self.center = gh.mirrorPoint(self.center, gh.obtainCenterOfPoints(centers))
        elif self.defects == 2:  # 3 Fingers
            centers = [self.firstFinger, self.secondFinger, self.lastFinger]
            self.center = gh.mirrorPoint(self.center, gh.obtainCenterOfPoints(centers))
        elif self.defects == 3:  # 4 Fingers
            centers = [self.firstFinger, self.secondFinger, self.middleFinger, self.lastFinger]
            self.center = gh.mirrorPoint(self.center, gh.obtainCenterOfPoints(centers))
        elif self.defects == 4:  # 5 Fingers
            centers = [self.firstFinger, self.secondFinger, self.middleFinger, self.fourthFinger, self.lastFinger]
            self.center = gh.mirrorPoint(self.center, gh.obtainCenterOfPoints(centers))
