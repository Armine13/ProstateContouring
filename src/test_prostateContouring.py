from prostateContouring import *
#import dicom
import pylab
from skimage import io


#im = dicom.read_file("../3D_T2/Image00033")
im = io.imread("im31.png")
original = im

#im = dicom.read_file("../3D_T2/Image00032")
#im = io.imread("prostate36.png")
#im = im.pixel_array

xCenter = 187
yCenter = 147

cont = ProstateContouring(im, yCenter, xCenter)
polars = cont.polarFromContourImage(io.imread('contour.png'))
angles = polars[:,0]
radii = polars[:,1]

cont.readModelShape(polars)

edgeIm = cont.detectEdges(1)

sigma = 5
cont.get_narrowContSearchPxl(sigma)


cont.filterOrientation(np.deg2rad(10))
cont.filterContinuity(polars, 3)

#pylab.imshow(cont.image, cmap='gray')
#pylab.show()

im = cont.fillMissingArea()
#print (np.nonzero(im))
cont.createContour()

#pylab.imshow(original, cmap=pylab.gray())
#pylab.imshow(cont.image,interpolation='none',alpha=0.5)
pylab.imshow(cont.image, cmap=pylab.gray())
pylab.show()
