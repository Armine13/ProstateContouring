# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pylab
import dicom
import os
import numpy as np
from matplotlib import pyplot, cm


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
        
pylab.imshow(DS[0].pixel_array, cmap=pylab.cm.bone)
pylab.show()