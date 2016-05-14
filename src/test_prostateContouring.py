from prostateContouring import *
#import dicom
import pylab
from skimage import io

#im = dicom.read_file("../3D_T2/Image00032")
im = io.imread("prostate36.png")
#im = im.pixel_array

xCenter = 187
yCenter = 147

cont = ProstateContouring(im, yCenter, xCenter)
polars = cont.polarFromContourImage(io.imread('contour.png'))
cont.readModelShape(polars)

cont.detectEdges()

cont.get_narrowContSearchPxl(10)

cont.filterOrientation(np.deg2rad(20))
cont.filterContinuity(polars, 3)

pylab.imshow(cont.image, cmap='gray')
pylab.show()

