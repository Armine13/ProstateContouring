# -*- coding: utf-8 -*-
"""
Created on Tue May 10 22:39:10 2016

@author: Mins
"""

#%%
"""List of functions
        class ProstateContouring
            polarFromContourImage(self, contIm)
            readModelShape(self, array)
            detectEdges(self)
            get_narrowContSearchPxl(self, s = 10)
            filterOrientation(self, sigma_angle = np.deg2rad(15))
        other
            skeletonOrientation(skel)
"""

import numpy as np
from skimage import measure
from skimage import feature

class ProstateContouring:
    def __init__(self, array, cy, cx):
        self.image = array
        self.xCenter = cx
        self.yCenter = cy

    def polarFromContourImage(self, contIm):
        #""""
            #Takes a contour image and returns array of corresponding
            #polar coordinates: angle, radius, orientation of edge
        #""""

        pol = np.empty((0,3), int)
        sz = np.shape(contIm)

        #Find orientations in contour image
        contO = skeletonOrientation(contIm)

        cx = self.xCenter
        cy = self.yCenter

        #For each non-zero pixel in image, extract radius, angle and orientation
        # relative to center
        for i in range(0, sz[0]):
            for j in range(0, sz[1]):
                if contIm[i, j] > 0:
                    r = np.sqrt((i - cy)**2 + (j - cx)**2)
                    dy = i - cy
                    dx = j - cx
                    th = np.arctan2(-dy, dx)
                    pol = np.append(pol, np.array([[th, r, contO[i, j]]]), axis=0)

        #Sort by increasing angles
        pol = pol[pol[:,0].argsort()]

        return pol
        #pol9 = np.empty((0,2), int)
        #a = 180
        #for i in range(20, 0, -1):

            #temp = out;
            #temp = out[np.rad2deg(out[:,0]) > (i-1)*9,:];
            #temp = temp[np.rad2deg(temp[:,0]) <= i*9,:];
            #for k in range(1, 10):
                #pol9 = np.append(pol9, np.array([[np.deg2rad(a), np.mean(temp[:,1], axis=0)]]), axis=0)
                #a = a - 1

        #for i in range(1, 21):
            #temp = out;
            #temp = out[np.rad2deg(out[:,0]) <= -(i-1)*9,:];
            #temp = temp[np.rad2deg(temp[:,0]) > -i*9,:];
            #for k in range(1, 10):
                #pol9 = np.append(pol9, np.array([[np.deg2rad(a), np.mean(temp[:,1], axis=0)]]), axis=0)
                #a = a - 1
        #return pol9

    def readModelShape(self, array):
        """ Takes the file containing prostate shape in polar coordinates"""
        #self.polCoor = array
        self.angles = array[:, 0]
        self.radii = array[:, 1]
        self.orients = array[:,2]

    def detectEdges(self):
        self.image = feature.canny(self.image, sigma=1.0, low_threshold=0.001, high_threshold=0.005)
        return self.image

    def get_narrowContSearchPxl(self, s = 10):
        self.sigma = s
        sz = np.shape(self.image)
        newIm = np.zeros(sz)

        for i in range(0, self.radii.shape[0]):
            x = int(np.round(self.xCenter+self.radii[i]*np.cos(self.angles[i])))
            y = int(np.round(self.yCenter+self.radii[i]*np.sin(-self.angles[i])))

            for j in range(-self.sigma, +self.sigma+1):
                for k in range(-self.sigma, self.sigma+1):
                    if x + j >= 0 and x + j < sz[1] and y + k >= 0 and y + k < sz[0]:
                        newIm[y + k, x + j] = self.image[y + k, x + j]
        self.image = newIm
        return self.image

    def filterOrientation(self, sigma_angle = np.deg2rad(15)):
        """"
            Filters out edges from array im, keeping edges that are oriented similarly to
            the edges in shapeContourIm(with permissible standard deviation sigma_angle)
        """
        #Extract orientations from current image
        imageOrients = skeletonOrientation(self.image)

        #find all non-zero elements of edge image
        pts = np.transpose(np.nonzero(self.image))

        #loop over all non-zero elements in edge image
        for (y, x) in pts:
            #Find angle of the pixel, relative to selected center point
            dy = y - self.yCenter
            dx = x - self.xCenter
            th = np.arctan2(-dy, dx)

            #find corresponding orientation value in model contour
            (idx, t) = min(enumerate(self.angles), key=lambda x: abs(x[1]-th))
            orient = self.orients[idx]

            #compare orientation at pt (x,y) to orientation in model contour
            #if they are different, set pixel to 0
            if not (imageOrients[y, x] <= orient + sigma_angle and imageOrients[y, x] >= orient - sigma_angle):
                self.image[y, x] = 0
        return self.image

    #def contourFromPolar(self):
        ##Creating the shape info image
        #stdShape = np.zeros(np.shape(self.image)) #same size as input image
        #for i in range(0, self.radii.shape[0]):
            #stdShape[int(np.round(self.yCenter-self.radii[i]*np.sin(self.angles[i]))),
                #int(np.round(self.xCenter+self.radii[i]*np.cos(self.angles[i])))] = 1
        #return stdShape

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
