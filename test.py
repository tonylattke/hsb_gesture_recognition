#!/usr/bin/python

# Python Libraries
import sys								# System 
import numpy as np 						# Functions for images
import cv2								# OpenCV
from matplotlib import pyplot as plt 	# Interface
import math								# Math operations

# Our Libraries
import colors_helpers as ch 			# Colors helpers

# Define colors
red = ch.colors['red']
green = ch.colors['green']
blue = ch.colors['blue']

# Main program
def main():
	# Default fileName
	fileName = 'images/hand.jpg'

	# Default blurring level
	blurringLevel = 35

	# Get file
	if len(sys.argv) > 1:
	    fileName = sys.argv[1]

	# Load image
	img = cv2.imread(fileName)

	# Croping
	#cv2.rectangle(img,(550,600),(50,50),(0,255,0),0)

	crop_img = img#[50:600, 50:550]

	# Gray
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

	# Blurring
	value = (blurringLevel,blurringLevel)
	blurred = cv2.GaussianBlur(gray, value, 0)

	# Threshold - Black and white
	_, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	# Contours
	contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cnt = max(contours, key = lambda x: cv2.contourArea(x))
	x,y,w,h = cv2.boundingRect(cnt)
	cv2.rectangle(crop_img,(x,y),(x+w,y+h),blue,0)
	drawing = np.zeros(crop_img.shape,np.uint8)
	cv2.drawContours(drawing,[cnt],0,green,0)

	# Convex Hull
	hull = cv2.convexHull(cnt)
	cv2.drawContours(drawing,[hull],0,red,0)

	# Render
	all_img = np.hstack((drawing, crop_img))
	cv2.imshow('Contours', all_img)

	# Exit
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# Run main program
main()