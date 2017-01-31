# HSB - Computational Geometry
# Professor: Martin Hering-Bertram
# Authors:  Filips Mindelis
#           Tony Lattke

# Python Libraries
import cv2  # OpenCV

# Our Libraries


class HandModel:
    defects = []  # Coordinates of defects
    triangles = []  # Triangles (lines connected with the defect)
    fingers = []  # Coordinates of finger
    centerOfHand = None
    angles = []
    numberOfFingers = 0
    contours = None

    def __init__(self):
        self.resetModel()
        print("Model of the hand created")

    def draw(self, image, colors, lineThickness, radious):
        # Surface of the hand
        if self.contours != None and len(self.contours) > 0:
            cv2.drawContours(image, self.contours, -1, colors['handSurface'], -1)

        # Triangles
        for triangle in self.triangles:
            cv2.line(image, triangle.cent, triangle.rect1, colors['finger'], lineThickness)
            cv2.line(image, triangle.cent, triangle.rect2, colors['finger'], lineThickness)

        # Fingers
        for finger in self.fingers:
            cv2.circle(image, finger, radious['finger']['intern'], colors['fingerPoint'], radious['finger']['extern'])

        # Defects
        for defect in self.defects:
            cv2.circle(image, defect, radious['defect']['intern'], colors['defect'], radious['defect']['extern'])

        # Center of the hand
        if self.centerOfHand != None:
            cv2.circle(image, self.centerOfHand, radious['centerOfHand']['intern'], colors['center'],
                       radious['centerOfHand']['extern'])

    def resetModel(self):
        self.defects = []  # Coordinates of defects
        self.triangles = []  # Triangles (lines connected with the defect)
        self.fingers = []  # Coordinates of finger
        self.centerOfHand = None
        self.angles = []
        self.numberOfFingers = 0
        self.contours = None
