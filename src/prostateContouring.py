# -*- coding: utf-8 -*-
"""
Created on Tue May 10 22:39:10 2016

@author: Mins
"""

#%%
"""Import libraries
"""

import numpy as np
from skimage import measure
from skimage import feature
from scipy import io

"""Create a class"""
class ProstateContouring:
    def __init__(self, array):
        self.image = array

    def setCenter(self, cy, cx):
        self.xCenter = cx
        self.yCenter = cy

    def setShapeFromFile(self, filename):
        """ Takes the file containing prostate shape in polar coordinates"""
        self.polCoor = io.loadmat(filename)["out"]
        self.angles = self.polCoor[:, 0]
        self.radii = self.polCoor[:, 1]

    def setShapeFromArray(self, array):
        """ Takes the file containing prostate shape in polar coordinates"""
        self.polCoor = array
        self.angles = array[:, 0]
        self.radii = array[:, 1]

    def readShape(self, contourImage):
        """ Reads a binary contour imagee and returs the polar coordinates of
            the shape in two columns:
            angle in radians and radii
        """
    def detectEdges(self):
        self.image = feature.canny(self.image, sigma=1.0, low_threshold=0.001, high_threshold=0.005)
        #edges_img = feature.canny(im, sigma=1.0, low_threshold=0.001, high_threshold=0.005)
        #edges_rescale = feature.canny(im_rescale, sigma=1.0, low_threshold=0.1, high_threshold=0.4)
        #edges_equ = feature.canny(im_equ, sigma=1.0, low_threshold=0.1, high_threshold=0.4)
        #edges_adapteq = feature.canny(im_adapteq, sigma=1.0, low_threshold=0.1, high_threshold=0.4)

    def get_narrowContSearchPxl(self, s = 10):

        sz = np.shape(self.image)
        newIm = np.zeros(sz)

        for i in range(0, self.radii.shape[0]):
            for j in range(-s, s):
                x = int(np.round(self.xCenter+self.radii[i]*np.cos(
                    self.angles[i])+j*np.cos(self.angles[i])))
                y = int(np.round(self.yCenter+self.radii[i]*np.sin(
                    -self.angles[i])+j*np.sin(-self.angles[i])))
                newIm[y, x] = self.image[y, x]

        self.image = newIm

    def createContourFromPolar(self):
        #Creating the shape info image

        stdShape = np.zeros(np.shape(self.image)) #same size as input image
        for i in range(0, self.radii.shape[0]):
            stdShape[int(np.round(self.yCenter-self.radii[i]*np.sin(self.angles[i]))),
                int(np.round(self.xCenter+self.radii[i]*np.cos(self.angles[i])))] = 1
        return stdShape

    def filterOrientation(self, sigma = 10, sigma_angle = 10):
        """"
            Filters out edges from array im, keeping edges that are oriented similarly to
            the edges in shapeContourIm(with permissible standard deviation sigma_angle)
        """
        shapeContourIm = self.createContourFromPolar()
        stdShapeOrient = skeletonOrientation(shapeContourIm)
        imOrient = skeletonOrientation(self.image)

        for i in range(0,self.radii.shape[0]):
            for j in range(-sigma, sigma):
                #Retrieve correct orientation for current angle
                stdOr = stdShapeOrient[int(np.round(self.yCenter-self.radii[i]*
                    np.sin(self.angles[i]))), int(np.round(self.xCenter+self.radii[i]*np.cos(self.angles[i])))]

                y = int(np.round(self.yCenter+self.radii[i]*np.sin(-self.angles[i])+j*np.sin(-self.angles[i])))
                x = int(np.round(self.xCenter+self.radii[i]*np.cos(self.angles[i])+j*np.cos(self.angles[i])))
                #if orientation at current pixel is not in permissible range, set pixel to 0
                if not (self.image[y, x] > 0 and imOrient[y, x] <=
                    stdOr + sigma_angle and imOrient[y, x] >= stdOr - sigma_angle):
                    self.image[y, x] = 0

def skeletonOrientation(skel):
    """
        Independent function that returns array of orientations of each pixel in edges of image skel
    """
    #http://fr.mathworks.com/matlabcentral/answers/88714-how-to-find-the-direction-angle-of-points-on-an-edge-in-a-digital-image

    #Error checking:
    sz = np.shape(skel)

    blksz  = np.array([5, 5])

    #Find the skeleton pixels' index
    [row, col] = np.nonzero(skel)
    npts = len(row)

    #Pad the array and offset the rows/cols so every local block fits
    padAmount = blksz // 2#distance from center to edge of block
    skelPad = np.pad(skel, [(padAmount[0], padAmount[0]), (
        padAmount[1], padAmount[1])], mode='constant')

    #Preallocate Orientations
    Orientations = np.zeros(sz)

    #Some parameters
    #-Bottom of block will be the same as center before pad
    #-Top will be bottom + block size - 1 (inclusive
    rowHigh = row + blksz[0] - 1
    colHigh = col + blksz[1] - 1
    center = padAmount + 1 #Center of small block

    for ii in np.arange(0, npts):
        #Extract small block
        block = skelPad[row[ii]:rowHigh[ii] + 1, col[ii]:colHigh[ii] + 1]

        #Label and calculate orientation
        Label = measure.label(block)

        #only label of center pixel
        center_label = (Label == Label[center[0], center[1]]).astype(int)

        rp = measure.regionprops(center_label)

        #Set orientation of the center pixel equal to the calculated one
        Orientations[row[ii], col[ii]] = rp[0].orientation
    return Orientations
#------------------------------------------------------------------------------
