# -*- coding: utf-8 -*-
"""
Created on Tue May 17 22:46:26 2016

@author: Yanik
"""

import dicom
import os
import numpy as np

class readDICOMfiles:
    def __init__(self, path):
        self.folderPath = path
        self.image_scaled = []
        
    def readFolder(self):
        """
        Read Dicom volume
        """
        self.DS = [] #list of all images
        PathDicom = self.folderPath
        lstFilesDCM = []  # create an empty list
        for dirName, subdirList, fileList in os.walk(PathDicom):
            for (i, filename) in enumerate(fileList):
                path = os.path.join(dirName,filename)
        #        lstFilesDCM.append(path) # List of file names+path
                self.DS.append(dicom.read_file(path))
                
    def rescaleImg(self,num):
        """Select an image in the volume"""
        im = self.DS[num].pixel_array       
        plan = self.DS[num]
        shape = plan.pixel_array.shape
        
        """Rescale in png shape"""
        image = []
        max_val = 0
        for row in plan.pixel_array:
            pixels = []
            for col in row:
                pixels.append(col)
                if col > max_val: max_val = col
            image.append(pixels)
                
        # Rescalling greyscale between 0-255
        self.image_scaled = []
        for row in image:
            row_scaled = []
            for col in row:
                col_scaled = int((float(col)/float(max_val))*255.0)
                row_scaled.append(col_scaled)
            self.image_scaled.append(row_scaled)
            
        return self.image_scaled
            
        