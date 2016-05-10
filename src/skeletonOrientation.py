
def createContourFromPolar(center, angles, radii, sz):
    #Creating the shape info image
    yCenter = center[0]
    xCenter = center[1]
    
    stdShape = np.zeros(sz)
    for i in range(0, radii.shape[0]):
        stdShape[int(np.round(yCenter-radii[i]*np.sin(angles[i]))), int(np.round(xCenter+radii[i]*np.cos(angles[i])))] = 1
    return stdShape
    
def skeletonOrientation(skel):
    #Error checking:
    sz = np.shape(skel)
    
    blksz  = np.array([5, 5])
    
    #Find the skeleton pixels' index
    [row, col] = np.nonzero(skel)
    npts = len(row)
    
    #Pad the array and offset the rows/cols so every local block fits
    padAmount = blksz // 2#distance from center to edge of block
    skelPad = np.pad(skel, [(padAmount[0], padAmount[0]), (padAmount[1], padAmount[1])], mode='constant')
    
    #Preallocate Orientations
    Orientations = np.zeros(sz)
    
    #Some parameters
    #-Bottom of block will be the same as center before pad
    #-Top will be bottom + block size - 1 (inclusive    
    rowHigh = row + blksz[0] - 1
    colHigh = col + blksz[1] - 1
    center = padAmount + 1#Center of small block
    
    for ii in np.arange(0, npts):
        #Extract small block
        block = skelPad[row[ii]:rowHigh[ii]+1, col[ii]:colHigh[ii]+1]
    
        #Label and calculate orientation
        Label = measure.label(block)
    
        #only label of center pixel
        center_label = (Label == Label[center[0], center[1]]).astype(int)
        
        rp = measure.regionprops(center_label)
        
        #Set orientation of the center pixel equal to the calculated one
        Orientations[row[ii], col[ii]] = rp[0].orientation
#    pylab.imshow(Orientations)
    return Orientations
    


def filterOrientation(im, shapeContourIm, radii, angles, center, sigma, sigma_angle):
    """"
    Filters out edges from array im, keeping edges that are oriented similarly to
    the edges in shapeContourIm(with permissible standard deviation sigma_angle)
    """    
    yCenter = center[0]
    xCenter = center[1]
    stdShapeOrient = skeletonOrientation(shapeContourIm)
    imOrient = skeletonOrientation(im)

    for i in range(0,radii.shape[0]):
        for j in range(-sigma, sigma):
            #Retrieve correct orientation for current angle                
            stdOr = stdShapeOrient[int(np.round(yCenter-radii[i]*np.sin(angles[i]))), int(np.round(xCenter+radii[i]*np.cos(angles[i])))]
            y = int(np.round(yCenter+radii[i]*np.sin(-angles[i])+j*np.sin(-angles[i])))
            x = int(np.round(xCenter+radii[i]*np.cos(angles[i])+j*np.cos(angles[i])))
            #if orientation at current pixel is not in permissible range, set pixel to 0                
            if not (im[y, x] > 0 and imOrient[y, x] <= stdOr + sigma_angle and imOrient[y, x] >= stdOr - sigma_angle):
                im[y, x] = 0
    return im


import numpy as np
import pylab
from scipy import io
from skimage import measure
from PIL import Image

I = Image.open('canny.png') 
#convert image to (0-1)
I = np.asarray(I) / np.max(np.max(I))
xCenter = 187
yCenter = 110
center = [yCenter, xCenter]
polCoor = io.loadmat("th_r.mat")["out"]
angles = polCoor[:,0]
radii = polCoor[:,1]

stdShapeIm = createContourFromPolar(center, angles, radii, np.shape(I))

s = 10 #std of radii
s_angle = np.deg2rad(2) #std for region of permissible angle

I = filterOrientation(I, stdShapeIm, radii, angles, center, s, s_angle)
    
#pylab.imshow(stdShapeOrient)
pylab.imshow(I)
pylab.show()