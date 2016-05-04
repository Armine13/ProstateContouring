# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import dicom
import os
import numpy as np

import pylab as pl

import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

from skimage import feature
from skimage import filters
from skimage import io
from skimage import exposure
from skimage import img_as_float, img_as_int

#ds = dicom.read_file("3D_T2/Image00001")
#ds2 =dicom.read_file("3D_T2/Image00002")

#rows = ds.Rows
#cols = ds.Columns
#print ds.pixel_array %returns matrix
#print ds.InstanceNumber 
#print ds2.InstanceNumber

matplotlib.rcParams['font.size'] = 8

"""
Functiun to plot img and histogram at same time
"""
def plot_img_and_hist(img, axes, bins=256):
    """Plot an image along with its histogram and cumulative histogram.

    """
    img = img_as_float(img)
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()
    
    # Display image
    ax_img.imshow(img, cmap=plt.cm.gray)
    ax_img.set_axis_off()
    ax_img.set_adjustable('box-forced')

    # Display histogram
    ax_hist.hist(img.ravel(), bins=bins, histtype='step', color='black')
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Pixel intensity')
    ax_hist.set_xlim(0, 1)
    ax_hist.set_yticks([])

    # Display cumulative distribution
    img_cdf, bins = exposure.cumulative_distribution(img, bins)
    ax_cdf.plot(bins, img_cdf, 'r')
    ax_cdf.set_yticks([])

    return ax_img, ax_hist, ax_cdf

#%%
"""
Read Discom images
"""
DS = [] #list of all images
PathDicom = "../3D_T2/"
lstFilesDCM = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicom):
    for (i, filename) in enumerate(fileList):
        path = os.path.join(dirName,filename)
#        lstFilesDCM.append(path) # List of file names+path
        DS.append(dicom.read_file(path))
N = i #number of images

"""
Display 17th image
"""
k = 17
im = DS[k].pixel_array
im = img_as_float(im)
#plt.figure()
#plt.imshow(im, cmap=pl.cm.bone)
#plt.show()



#%%
"""
Apply different contrast
"""
#Contrast stretching
p2, p98 = np.percentile(im, (2,98))
im_rescale = exposure.rescale_intensity(im, in_range=(p2,p98))
#Equalization
im_equ = exposure.equalize_hist(im)
#Adaptive Equalization
im_adapteq = exposure.equalize_adapthist(im, clip_limit=0.03)
#io.imsave("prostate.png", im*255)

#%%
"""
Display results
"""
fig = plt.figure(figsize=(8, 5))
axes = np.zeros((2,4), dtype=np.object)
axes[0,0] = fig.add_subplot(2, 4, 1)
for i in range(1,4):
    axes[0,i] = fig.add_subplot(2, 4, 1+i, sharex=axes[0,0], sharey=axes[0,0])
for i in range(0,4):
    axes[1,i] = fig.add_subplot(2, 4, 5+i)
    
ax_img, ax_hist, ax_cdf = plot_img_and_hist(im, axes[:, 0])
ax_img.set_title('Low contrast image')

y_min, y_max = ax_hist.get_ylim()
ax_hist.set_ylabel('Number of pixels')
ax_hist.set_yticks(np.linspace(0, y_max, 5))

ax_img, ax_hist, ax_cdf = plot_img_and_hist(im_rescale, axes[:, 1])
ax_img.set_title('Contrast stretching')

ax_img, ax_hist, ax_cdf = plot_img_and_hist(im_equ, axes[:, 2])
ax_img.set_title('Histogram equalization')

ax_img, ax_hist, ax_cdf = plot_img_and_hist(im_adapteq, axes[:, 3])
ax_img.set_title('Adaptive equalization')

ax_cdf.set_ylabel('Fraction of total intensity')
ax_cdf.set_yticks(np.linspace(0, 1, 5))

# prevent overlap of y-axis labels
fig.subplots_adjust(wspace=0.4)
plt.show()

#%%
"""
Canny edge detection
"""
edges_img = feature.canny(im, sigma=1.0, low_threshold=0.001, high_threshold=0.005)
edges_rescale = feature.canny(im_rescale, sigma=1.0, low_threshold=0.1, high_threshold=0.4)
edges_equ = feature.canny(im_equ, sigma=1.0, low_threshold=0.1, high_threshold=0.4)
edges_adapteq = feature.canny(im_adapteq, sigma=1.0, low_threshold=0.1, high_threshold=0.4)

#%%
"""
Display results
"""
fig = plt.figure(figsize=(15, 8))
axes = np.zeros((2,4), dtype=np.object)
axes[0,0] = fig.add_subplot(2, 4, 1)
for i in range(1,4):
    axes[0,i] = fig.add_subplot(2, 4, 1+i, sharex=axes[0,0], sharey=axes[0,0])
    
axes[0, 0].imshow(edges_img, cmap=plt.cm.gray)
axes[0, 0].set_title('Low contrast image')
axes[0, 0].set_axis_off()
axes[0, 0].set_adjustable('box-forced')

axes[0, 1].imshow(edges_rescale, cmap=plt.cm.gray)
axes[0, 1].set_title('Contrast stretching')
axes[0, 1].set_axis_off()
axes[0, 1].set_adjustable('box-forced')

axes[0, 2].imshow(edges_equ, cmap=plt.cm.gray)
axes[0, 2].set_title('Histogram equalization')
axes[0, 2].set_axis_off()
axes[0, 2].set_adjustable('box-forced')

axes[0, 3].imshow(edges_adapteq, cmap=plt.cm.gray)
axes[0, 3].set_title('Adaptive equalization')
axes[0, 3].set_axis_off()
axes[0, 3].set_adjustable('box-forced')

# prevent overlap of y-axis labels
fig.subplots_adjust(wspace=0.4)
plt.show()

#%% 
"""
Get click on image
"""


coords = []

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print 'x = %d, y = %d'%(
        ix, iy)

    global coords
    coords.append((ix, iy))

    if len(coords) == 2:
        fig.canvas.mpl_disconnect(cid)

    return coords
    
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(edges_equ, cmap=pl.cm.bone)
#plt.ion()
#plt.show()

#ix = []
#iy= []


plt.show()

cid = fig.canvas.mpl_connect('button_press_event', onclick)


#%%
"""
Try to draw
"""
#pl.plot([1,2,3])
#pl.xlabel('hi mom')
#
##create big-expensive-figure
#pl.ioff()      # turn updates off
#pl.title('now how much would you pay?')
## xticklabels(fontsize=20, color='green')
#pl.draw()      # force a draw
#pl.savefig('alldone', dpi=300)
#pl.close()
#pl.ion()      # turn updating back on
#pl.plot(pl.rand(20), mfc='g', mec='r', ms=40, mew=4, ls='--', lw=3)