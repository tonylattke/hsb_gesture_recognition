# Python Libraries
import numpy as np  # Functions for images
import cv2          # OpenCV

# Our Libraries
import geometry_helpers as gh
import colors_helpers as ch
import Triangle as th
import FilipsModel as hfm
import TonyModel as htm

# Image Processor
class ImageProcessor:
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

    crooping = True
    fileName = 'images/hand.jpg'

    numberOfFingers = 0

    def __init__(self):
        print "Image processor ready"

# Main program
def analyze(ip):
    # Initialization
    crooping = ip.crooping
    fileName = ip.fileName
    croopingWidth = ip._croopingWidth
    croopingHeight = ip._croopingHeight
    croopingX = ip._croopingX
    croopingY = ip._croopingY

    # Load image
    img = cv2.imread(fileName)

    # Croping
    crop_img = img

    if crooping:
        cv2.rectangle(img, (croopingWidth, croopingHeight), (croopingX, croopingY), ip.cyan, ip.lineThicknessCrooping)
        crop_img = img[croopingY:croopingHeight, croopingX:croopingWidth]

    # Grayscale
    grayscale = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Blurring
    value = (ip.blurringLevel, ip.blurringLevel)
    blurred = cv2.GaussianBlur(grayscale, value, 0)

    # Threshold - Black and white
    _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    if thresh1 is not None:
        # Contours
        contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cnt = 0
        try:
            global cnt
            cnt = max(contours, key=lambda x: cv2.contourArea(x))
        except (ValueError, TypeError):
            print('empty list or invalid input')
            cnt = 0

        if cnt is not 0:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(crop_img, (x, y), (x + w, y + h), ip.blue, ip.lineThickness)
            drawing = np.zeros(crop_img.shape, np.uint8)
            cv2.drawContours(drawing, [cnt], 0, ip.green, ip.lineThickness)

            # Convex Hull
            hull = cv2.convexHull(cnt)
            cv2.drawContours(drawing, [hull], 0, ip.red, ip.lineThickness)

            # Calculate Defect points
            hullWithoutPoints = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hullWithoutPoints)
            count_defects = 0
            triangles = []
            if defects is not None:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    angle = gh.calculateAngle(start,end,far)
                    if angle <= 90:
                        count_defects += 1
                        triangle = th.Triangle(start,end,far)
                        triangles.append(triangle)
                    cv2.line(crop_img, start, end, ip.red, ip.lineThickness)

            # Calculate center of hand
            centerOfHand = th.listToTuple(th.obtainCenterOfHand(triangles))

            handModel = hfm.FilipsModel(centerOfHand,triangles)
            ip.numberOfFingers = handModel.countOfFinger()
            handModel.getCenter()
            handModel.drawLines(drawing, ip.magenta, ip.lineThickness)
            handModel.drawDefects(drawing, ip.yellow, ip.defectInternRadius, ip.defectExternRadius)
            handModel2 = htm.TonyModel(handModel.center, triangles)
            handModel2.drawLines(drawing, ip.cyan, ip.lineThickness)

            # cv2.imshow('Contours', all_img)
            cv2.imwrite("drawing.png", drawing)
            cv2.imwrite("crop_img.png", crop_img)
