# -*- coding: utf-8 -*-
"""
Created on Thu May  5 15:46:29 2016

@author: Yanik
"""

from tkinter import * #Change for Tkinter if python 2
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

#from skimage import io
import scipy.io as spio
#from skimage import io
#import io
#from StringIO import StringIO

import numpy as np

#File = "C:\Users\Yanik\Documents\GitHub\ProstateContouring\src\prostateRescaled.png"
fenetre = Tk()
#File = askopenfilename(parent=fenetre, initialdir="C:/",title='Choose an image.')
File = "C:/Users/Yanik/Documents/GitHub/ProstateContouring/src/prostateRescaled.png"
img = Image.open(File)
#imgTk = ImageTk.PhotoImage(img)
"""Convert image to list"""
pixels = list(img.getdata())
width, height = img.size
pixels2 = [pixels[i * width:(i + 1) * width] for i in range(1,height)]

"""Convert image to numpy array"""
imgarray = np.asarray(img.getdata(), np.uint16)
#for i in range(0,height-1)
#    imgarray[i,:] = imgarray[i * width:(i+1) * width,1]
imgArray2 = np.reshape(imgarray, (height, width), order='A')

"""Try to set array data"""
for i in range(1,100):
    for j in range(1,100):
        imgArray2[i,j]=0
#imgarray = [imgarray[i * width:(i + 1) * width] for i in range(1,height)]
#io.imsave("imgArray.png", imgArray2)

"""Load mat data for polar coordinates of prostate shape"""
polCoor = spio.loadmat("th_r.mat")
polCoor9 = spio.loadmat("th_r_9.mat")

 
#imgRecovered = Image.open(io.StringIO(pixels))
imgRecov = Image.new(img.mode, img.size)
imgRecov.putdata(pixels2)
fenetre.mainloop()
