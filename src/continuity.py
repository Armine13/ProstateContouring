# -*- coding: utf-8 -*-
"""
Created on Wed May 11 11:20:20 2016

@author: Yanik
"""

import numpy as np
import pylab
from scipy import io
from skimage import measure
from skimage import io as scio
from PIL import Image
import matplotlib.pyplot as plt
from skimage import img_as_float

""""import image from file and rescale it [0-1]"""
pilI = Image.open("orientation.png")
arI = np.asarray(pilI) / np.max(np.max(pilI))

"""import coordinates"""
xCenter = 187
yCenter = 110
center = [yCenter, xCenter]
polCoor = io.loadmat("th_r.mat")["out"]
angles = polCoor[:,0]
radii = polCoor[:,1]

"""Remove too small regions"""
labels_init = measure.label(arI)
max_lab = np.max(labels_init)
for m in range(1,max_lab+1):
    if((labels_init==m).sum()<3):
        mask = ~(labels_init==m)
        arI = arI*mask

"""Display first result"""
pylab.imshow(arI,cmap=plt.cm.gray)
pylab.show()

"""Preallocate variables"""
ray_w = 5 #width of the beam search
half_w = int(ray_w/2)
diag = np.zeros([102,ray_w])
new_img = arI
y = np.zeros(ray_w)
x = np.zeros(ray_w)


for i in range(0,len(angles)):
#for i in range(220,221):
    labels = measure.label(new_img, neighbors=8 )
    """Get labels in a diagonal beam"""
    for j in range(0,100):
        for s in range(-half_w,half_w+1):         
            y[s+1] = int(np.round(yCenter+(j+s)*np.sin(-angles[i])))
            x[s+1] = int(np.round(xCenter+(j+s)*np.cos(angles[i])))
            diag[j][s+1] = labels[y[s+1],x[s+1]]
#        y = int(np.round(yCenter+radii[i]*np.sin(-angles[i])+j*np.sin(-angles[i])))
#        x = int(np.round(xCenter+radii[i]*np.cos(angles[i])+j*np.cos(angles[i])))
        
    """Get number of labels in a beam""" 
    labDiag = np.array(list(set(diag[np.nonzero(diag)])))
    nLab = len(labDiag)
    
    """Get the size of each region detected"""
    rp = measure.regionprops(labels)
    sz_labels = np.zeros(nLab)
    for k in range(0,nLab):
        sz_labels[k] = (labels==labDiag[k]).sum()        
        #Discard the too small areas
#        if(sz_labels[k]<5):
#            ind_lab = ~(labels==labDiag[k])
#            new_img = new_img*ind_lab
#            nLab = nLab-1
#            sz_labels[k]=100
            
    """Discard the smallest edges if there are more than 1 edge in the beam"""       
    if(nLab>1):
        print (">1 label")                          
        #remove the smallest region from the image
        min_lab = np.argmin(sz_labels)
        ind_lab = ~(labels==labDiag[min_lab])
        new_img = new_img*ind_lab

pylab.imshow(new_img, cmap=plt.cm.gray)
scio.imsave("continu.png",new_img)
pylab.show()


