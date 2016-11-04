#!/usr/bin/python

import sys
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

fileName = 'hand.jpg'

if len(sys.argv) > 1:
    fileName = sys.argv[1]

img = cv2.imread(fileName)

# Croping
#cv2.rectangle(img,(550,600),(50,50),(0,255,0),0)

crop_img = img#[50:600, 50:550]

# Gray
gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

# Blurring
value = (35, 35)
blurred = cv2.GaussianBlur(gray, value, 0)

# Threshold - Black and white
_, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# Contours
contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cnt = max(contours, key = lambda x: cv2.contourArea(x))
x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
drawing = np.zeros(crop_img.shape,np.uint8)
cv2.drawContours(drawing,[cnt],0,(0,255,0),0)

# Convex Hull
hull = cv2.convexHull(cnt)
cv2.drawContours(drawing,[hull],0,(0,0,255),0)

# Render
cv2.imshow('Gesture', img)
all_img = np.hstack((drawing, crop_img))
cv2.imshow('Contours', all_img)

# Exit
cv2.waitKey(0)
cv2.destroyAllWindows()