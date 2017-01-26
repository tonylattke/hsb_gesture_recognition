# HSB - Computational Geometry
# Professor: Martin Hering-Bertram
# Authors:  Filips Mindelis
#           Tony Lattke

# Python Libraries
import pickle, time, os, threading
import numpy as np
from numpy import sqrt, arccos, rad2deg
import cv2

# Our Libraries
import TriangleN as tr
import HandModel as hm
import colors_helpers as ch
import math_helpers as mh

# HandTracking Processor class
class HandTracking:
    # Constructor
    def __init__(self):
        self.debugMode = True

        self.previousPosition = 0  # Get the relative position of mouse pointer

        # Data
        self.Data = {"angles less 90": 0,
                     "hulls": 0,
                     "defects": 0,
                     "fingers": 0,
                     "fingers history": []
                     }

        # Settings
        try:
            self.settings = pickle.load(open(".config", "r"))
        except:
            print "Config file not found."
            exit()

        # Create model of the hand
        self.hand = hm.HandModel()

    # imageProcessing - Run the image processing
    def imageProcessing(self, frame):
        # Settings reload
        try:
            self.settings = pickle.load(open(".config", "r"))
        except:
            print "Config file not found."
            exit()

        self.hand.resetModel()

        im = frame
        
        im = cv2.flip(im, 1)
        self.imOrig = im.copy()
        self.imNoFilters = im.copy()

        # Bluring
        im = cv2.blur(im, (self.settings["smooth"], self.settings["smooth"]))

        # Filtering the hand (Skin color)
        filter_ = self.filterSkin(im)

        # Erosion
        filter_ = cv2.erode(filter_,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                                      (self.settings["erode"], self.settings["erode"])))

        # Dilation
        filter_ = cv2.dilate(filter_,
                             cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                                       (self.settings["dilate"], self.settings["dilate"])))

        # Recognition of contours
        contours, hierarchy = cv2.findContours(filter_, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # Filtering the contours
        allIdex = []
        for index in range(len(contours)):
            area = cv2.contourArea(contours[index])
            if area < 5e3:
                allIdex.append(index)
        allIdex.sort(reverse=True)
        for index in allIdex:
            contours.pop(index)
        self.hand.contours = contours
        # No contours
        if len(contours) == 0:
            return

        # Getting Information of contours
        allIdex = []
        index_ = 0
        for cnt in contours:
            tempIm = im.copy()
            tempIm = cv2.subtract(tempIm, im)

            # Detect fingers
            hull = cv2.convexHull(cnt)
            self.last = None
            self.Data["hulls"] = 0
            for hu in hull:
                if self.last == None:
                    fingerPoint = tuple(hu[0])
                    self.hand.fingers.append(fingerPoint)
                else:
                    distance = mh.distance(self.last, tuple(hu[0]))
                    if distance > 40:  # Filtering Points
                        self.Data["hulls"] += 1
                        fingerPoint = tuple(hu[0])
                        self.hand.fingers.append(fingerPoint)
                self.last = tuple(hu[0])

            # Calculate the center of the hand
            M = cv2.moments(cnt)
            centroid_x = int(M['m10'] / M['m00'])
            centroid_y = int(M['m01'] / M['m00'])
            self.hand.centerOfHand = (centroid_x, centroid_y)

            # Calculate the defects (space between the fingers)
            hull = cv2.convexHull(cnt, returnPoints=False)
            angles = []
            defects = cv2.convexityDefects(cnt, hull)
            if defects == None:
                return

            # Generate the triangle, defect and angle list
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                if d > 1000:
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])
                    triangle = tr.TriangleN(far, start, end)
                    self.hand.triangles.append(triangle)
                    self.hand.defects.append(far)
                    self.hand.angles.append(triangle.angle())
            self.Data["defects"] = len(self.hand.defects)

            # Calculate the number of fingers
            anglesLess90 = filter(lambda a: a < 90, self.hand.angles)
            self.Data["angles less 90"] = len(anglesLess90)
            self.Data["fingers"] = len(anglesLess90) + 1

            self.Data["fingers history"].append(len(anglesLess90) + 1)
            self.hand.draw(tempIm, ch.colorSettings, 1, mh.radious)

            if len(self.Data["fingers history"]) > 10: self.Data["fingers history"].pop(0)
            self.imOrig = cv2.add(self.imOrig, tempIm)

            index_ += 1

        return self.imOrig

    # ----------------------------------------------------------------------
    def filterSkin(self, image):
        # LOWER = np.array([[0, 48, 80]], np.uint8)  # Hautfarbe untere Grenze
        # UPPER = np.array([[20, 255, 255]], np.uint8) # Hautfarbe obere Grenze
        # LOWER = np.array([[0,50,50]], np.uint8)  # Rot untere Grenze
        # UPPER = np.array([[10,255,255]], np.uint8)  # Rot obere Grenze
        # LOWER = np.array([[5,50,50]], np.uint8)  # Orange untere Grenze
        # UPPER = np.array([[15,255,255]], np.uint8)  # Orange obere Grenze
        LOWER = np.array([[0, 0, 0]], np.uint8)  # Schwarz untere Grenze
        UPPER = np.array([[180, 255, 35]], np.uint8)  # Schwarz obere Grenze
        # UPPER = np.array([self.settings["upper"], self.settings["filterUpS"], self.settings["filterUpV"]], np.uint8)
        # LOWER = np.array([self.settings["lower"], self.settings["filterDownS"], self.settings["filterDownV"]], np.uint8)
        hsv_im = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        filter_im = cv2.inRange(hsv_im, LOWER, UPPER)
        return filter_im

    # actionMouse - Action with mouse
    def actionMouse(self):
        # Times of repeated number of fingers
        times = 3
        # Left click - 5 Fingers
        if self.Data["fingers history"][:times] == [5] * times:
            os.system("xdotool click 1")
            self.Data["fingers history"] = [0]  # Clear history
        # Right click - 3 Fingers
        elif self.Data["fingers history"][:times] == [3] * times:
            os.system("xdotool click 3")
            self.Data["fingers history"] = [0]  # Clear history

    # updateMousePosition - Update the position of the mouse pointer
    def updateMousePosition(self):
        currentPosition = self.hand.centerOfHand
        if currentPosition is not None:
            previousPosition = self.previousPosition
            newPosition = np.subtract(currentPosition, previousPosition)
            self.previousPosition = currentPosition

            if self.Data["fingers"] in [1]:
                try:
                    self.t.__stop.set()
                except:
                    pass
                # Thread to update the position of mouse
                self.t = threading.Thread(target=self.moveMouse, args=(newPosition))
                self.t.start()

    # moveMouse - Move the mouse pointer
    def moveMouse(self, x, y):
        mul = 2
        x *= mul
        y *= mul
        stepp = 10
        if x > 0:
            for i in range(0, x, stepp):
                os.system("xdotool mousemove_relative -- %d %d" % (i, mh.smoothPositionY(x, y, i)))
        if x < 0:
            for i in range(x, 0, stepp):
                os.system("xdotool mousemove_relative -- %d %d" % (i, mh.smoothPositionY(x, y, i)))
        time.sleep(0.2)
