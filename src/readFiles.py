# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import dicom
import os
import numpy as np
from matplotlib import cm

import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage import feature
from skimage import filters
from skimage import io

#ds = dicom.read_file("3D_T2/Image00001")
#ds2 =dicom.read_file("3D_T2/Image00002")

#rows = ds.Rows
#cols = ds.Columns
#print ds.pixel_array %returns matrix
#print ds.InstanceNumber 
#print ds2.InstanceNumber

DS = [] #list of all images
PathDicom = "../3D_T2/"
lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for (i, filename) in enumerate(fileList):
        path = os.path.join(dirName,filename)
#        lstFilesDCM.append(path) # List of file names+path
        DS.append(dicom.read_file(path))
N = i #number of images

#Display 17th image
k = 17
im = DS[k].pixel_array
plt.figure()
plt.imshow(im, cmap=pylab.cm.bone)
plt.show()

#Canny edge detection

edges1 = feature.canny(im, sigma=1.0, low_threshold=10, high_threshold=100)

plt.figure()
plt.imshow(edges1, cmap=pylab.cm.bone)
plt.show()

io.imsave("prostate.png", im*255)