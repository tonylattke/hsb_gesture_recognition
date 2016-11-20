# Python Libraries
import cv2          # OpenCV

# Our Libraries
import Triangle as th

class TonyModel:
    center = None
    firstFinger = None
    secondFinger = None
    middleFinger = None
    fourthFinger = None
    lastFinger = None
    defects = 0

    def __init__(self,center,triangles):
        self.center = center
        self.defects = len(triangles)

        if self.defects == 0:
            pass
        elif self.defects == 1:
            self.firstFinger = triangles[0].fingerA
            self.lastDefect = triangles[0].fingerB
        elif self.defects == 2:
            self.firstFinger = triangles[0].fingerA
            self.secondFinger = th.averagePoint(triangles[0].fingerB,triangles[1].fingerA)
            self.lastFinger = triangles[1].fingerB
        elif self.defects == 3:
            self.firstFinger = triangles[0].fingerA
            self.secondFinger = th.averagePoint(triangles[0].fingerB, triangles[1].fingerA)
            self.middleFinger = th.averagePoint(triangles[1].fingerB, triangles[2].fingerA)
            self.lastFinger = triangles[2].fingerB
        elif self.defects == 4:
            self.firstFinger = triangles[0].fingerA
            self.secondFinger = th.averagePoint(triangles[0].fingerB, triangles[1].fingerA)
            self.middleFinger = th.averagePoint(triangles[1].fingerB, triangles[2].fingerA)
            self.fourthFinger = th.averagePoint(triangles[2].fingerB, triangles[3].fingerA)
            self.lastFinger = triangles[3].fingerB

    def drawLines(self,image,color,lineThickness):
        if self.defects == 0:
            pass
        elif self.defects == 1: # 2 Fingers
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.firstFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.lastFinger), color, lineThickness)
        elif self.defects == 2: # 3 Fingers
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.firstFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.secondFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.lastFinger), color, lineThickness)
        elif self.defects == 3: # 4 Fingers
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.firstFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.secondFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.middleFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.lastFinger), color, lineThickness)
        elif self.defects == 4: # 5 Fingers
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.firstFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.secondFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.middleFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.fourthFinger), color, lineThickness)
            cv2.line(image, th.listToTuple(self.center), th.listToTuple(self.lastFinger), color, lineThickness)