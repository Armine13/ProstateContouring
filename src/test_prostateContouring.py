from prostateContouring import *
import dicom
import pylab
#from skimage import *


im = dicom.read_file("../3D_T2/Image00017")
cont = ProstateContouring(im.pixel_array)
cont.setShapeFromFile("th_r.mat")
cont.detectEdges()
cont.setCenter(110, 187)

cont.get_narrowContSearchPxl(10)
cont.filterOrientation(10, np.deg2rad(20))

pylab.imshow(cont.image)
pylab.show()