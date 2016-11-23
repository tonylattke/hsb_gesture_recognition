#!/usr/bin/python

# Python Libraries
import sys  # System
import numpy as np  # Functions for images
import cv2  # OpenCV
from matplotlib import pyplot as plt  # Interface
import math  # Math operations
import gui

# Our Libraries
import colors_helpers as ch  # Colors helpers

# Define colors
red = ch.colors['red']
green = ch.colors['green']
blue = ch.colors['blue']
cyan = ch.colors['cyan']
magenta = ch.colors['magenta']
yellow = ch.colors['yellow']

# Line Thickness
lineThickness = 3
lineThicknessCrooping = 2

# Default Crooping
_croopingWidth = 550
_croopingHeight = 600
_croopingX = 50
_croopingY = 50

# Default blurring level
blurringLevel = 45

# Radius for defect points
defectInternRadius = 0
defectExternRadius = 10


# Calculates the distance between points
def distance(pointA, pointB):
    return math.sqrt((pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2)


# Main program
def main():
    # Initialization
    fileName = ''
    crooping = True

    # Get standart input
    if len(sys.argv) > 1:
        # File
        fileName = sys.argv[1]

        # Crooping
        if sys.argv[2] == '--noCrooping':
            crooping = False
        elif sys.argv[2] == '--crooping':
            croopingWidth = int(sys.argv[3])
            croopingHeight = int(sys.argv[4])
            croopingX = int(sys.argv[5])
            croopingY = int(sys.argv[6])
    else:
        fileName = 'images/hand.jpg'
        croopingWidth = _croopingWidth
        croopingHeight = _croopingHeight
        croopingX = _croopingX
        croopingY = _croopingY

    # Load image
    img = cv2.imread(fileName)

    # Croping
    crop_img = img

    if crooping:
        cv2.rectangle(img, (croopingWidth, croopingHeight), (croopingX, croopingY), cyan, lineThicknessCrooping)
        crop_img = img[croopingY:croopingHeight, croopingX:croopingWidth]

    # Grayscale
    grayscale = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Blurring
    value = (blurringLevel, blurringLevel)
    blurred = cv2.GaussianBlur(grayscale, value, 0)

    # Threshold - Black and white
    _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Contours
    contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key=lambda x: cv2.contourArea(x))
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x + w, y + h), blue, lineThickness)
    drawing = np.zeros(crop_img.shape, np.uint8)
    cv2.drawContours(drawing, [cnt], 0, green, lineThickness)
    # cv2.drawContours(crop_img,[cnt],0,green,lineThickness)

    # Convex Hull
    hull = cv2.convexHull(cnt)
    cv2.drawContours(drawing, [hull], 0, red, lineThickness)

    # Calculate Defect points
    hullWithoutPoints = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hullWithoutPoints)
    count_defects = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        a = distance(start, end)
        b = distance(far, start)
        c = distance(end, far)
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 60
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, defectInternRadius, yellow, defectExternRadius)
        cv2.line(crop_img, start, end, red, lineThickness)
    print(str(count_defects) + " Defects")

    # Render
    all_img = np.hstack((drawing, crop_img))
    # cv2.imshow('Contours', all_img)
    cv2.imwrite("drawing.png", drawing)
    cv2.imwrite("crop_img.png", crop_img)

    # Exit
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Run main program TODO: Namensgebung verbessern
main()
fi = gui.MainApp()
fi.run()
