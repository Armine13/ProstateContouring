# -*- coding: utf-8 -*-
"""
Created on Wed May 04 15:58:45 2016

@author: Yanik
"""

#%%
"""Import libraries
"""
#import numpy as np
from tkinter import * #Change for Tkinter if python 2
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk

import dicom
import os
import numpy as np
import pylab as pl

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

from skimage import img_as_float, img_as_ubyte
from skimage import io as skio
from skimage import feature
from skimage import exposure
from scipy import io

from prostateContouring import *
from readDICOMfiles import *
        
"""Create a class"""
class Interface(Frame):
    
    """class which is derived from a frame"""
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=500, height=450, **kwargs)
        self.pack(fill=BOTH)
        self.nb_clic = 0
        #Coordinates of pxl representing the contour
        self.xCoor = []
        self.yCoor = []
        
        #Coordinates of the prostate center
        self.xCenter = 0
        self.yCenter = 0
        #Coordinates of pxl inside narrow contour search
        self.xCont = []
        self.yCont = []
        
        #get contour shape average from file
        self.polCoor = io.loadmat("th_r.mat")["out"]
        self.angles2 = self.polCoor[:,0]
        self.radii2 = self.polCoor[:,1]
            
        self.isprocessed = False
        
        #Build widgets
        self.message = Label(self, text="Open an image", fg="red")
        self.message.grid(row=7,column=0,columnspan=1)
        
        
        self.button_open = Button(self, text="Open", command=self.openImg,
                                  width=10, height=1)
        self.button_open.grid(row=1,column=0,sticky=S+W)
        
        self.button_center = Button(self, text="Click center", state=DISABLED,
                                    command=self.click_center,width=10, height=1)
        self.button_center.grid(row=2,column=2)
        
        
        Label(self, text="From ").grid(row=3, column=3, sticky=W)
        self.fromSpin = Spinbox(self, from_=0, to=63, state=DISABLED, width=3)
        self.fromSpin.grid(row=3, column=3, sticky=E)
        Label(self, text=" to ").grid(row=3,column=5)
        self.toSpin = Spinbox(self, from_=0, to=63, state=DISABLED, width=3)
        self.toSpin.grid(row=3, column=6)
        
        self.button_prop = Button(self, text="Start", command=self.propagateContour,
                                  state=DISABLED, width=10, height=1)
        self.button_prop.grid(row=3,column=2,columnspan=1)        
        
        self.button_3d = Button(self, text="3D", fg="red", command=self.display3D,
                                state=DISABLED, width=10, height=1)
        self.button_3d.grid(row=5,column=2)
        
        self.button_modify = Button(self, text="Modify", state=DISABLED,
                                    command=self.modifyContour, width=10)
        self.button_modify.grid(row=4,column=2)
        
        self.button_stopModifying = Button(self,text="Done", state=DISABLED,
                                    command=self.stopModifying, width=10)
        self.button_stopModifying.grid(row=4,column=3)
        

        Label(self, text="Image n°").grid(row=0,column=1,sticky=S)       
        self.nSpin = Spinbox(self, width=7,from_=0, to=63, state=DISABLED,
                             command=self.go2img)
        self.nSpin.grid(row=1,column=1,sticky=S)
        
#        self.button_go = Button(self, text="Go", command=self.go2img,
#                                state=DISABLED)
#        self.button_go.grid(row=1,column=2,sticky=W)
        
        self.frame = Frame(self, bd=2, relief=SUNKEN,width=500,height=308)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.xscroll = Scrollbar(self.frame, orient=HORIZONTAL)
        self.xscroll.grid(row=1, column=0, sticky=E+W)
        self.yscroll = Scrollbar(self.frame)
        self.yscroll.grid(row=0, column=1, sticky=N+S)
        self.canvas = Canvas(self.frame, bd=0, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set,
                             width = 384, height = 308)
        self.canvas.grid(row=0, column=0, rowspan=1, sticky=N+S+E+W)
        self.xscroll.config(command=self.canvas.xview)
        self.yscroll.config(command=self.canvas.yview)
        self.frame.grid(row=2,column=0,columnspan=2, rowspan=6)

    def displayInCanvas(self, image):
        #Display in the canvas
        self.imgtk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0,0,image=self.imgtk,anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        
    def openImg(self):
        #open the directory and get the image from the dicom file    
        Dir = askdirectory(parent=fenetre, initialdir="C:/",title='Choose a directory.')
        self.dicomFiles = readDICOMfiles(Dir)
        self.dicomFiles.readFolder()
        self.imagePNG = np.asarray(self.dicomFiles.rescaleImg(32))
        self.img = Image.fromarray(self.imagePNG)
        self.width, self.height = self.img.size
        
        #initialize stack of contour images
        self.contour = np.zeros((self.height, self.width, 64), 'uint8')
        
        #Display in the canvas
        self.displayInCanvas(self.img)
        self.message["text"]="Now press on click center do segment this image"
        self.button_center.config(state=NORMAL) 
        
        self.nSpin.config(state=NORMAL)
        self.nSpin.delete(0,END)
        self.nSpin.insert(0,"32")
        self.nSpin.config(state="readonly")
        
#        self.fromSpin.config(state="readonly")
#        self.toSpin.config(state="readonly")
        
    def go2img(self):
        self.nImg = int(self.nSpin.get())
        image = np.asarray(self.dicomFiles.rescaleImg(self.nImg))

        if(self.isprocessed):
            """Build a rgb image with contour in blue on top of original image"""
            rgbImg = np.zeros((self.height, self.width, 3), 'uint8')
            rgbImg[...,0] = image
            rgbImg[...,1] = image
            rgbImg[...,2] = image
    
            index = np.nonzero(img_as_ubyte(self.contour[...,self.nImg]))
            print(self.nImg)
            rgbImg[index[0], index[1], 0] = 0
            rgbImg[index[0], index[1], 1] = 0
            rgbImg[index[0], index[1], 2] = 255
            
        else:            
            rgbImg = image
            
        """Convert back the result to PIL image and display in canvas"""    
        self.img = Image.fromarray(rgbImg)
        self.displayInCanvas(self.img)
        
    def click_center(self):
        self.canvas.bind("<Button 1>", self.getCenter)
        self.message["text"]="Click on the center"
               
    def getCenter(self, event):
        self.xCenter = event.x
        self.yCenter = event.y
#        self.compute_anglesAndRadii()
#        self.get_narrowContSearchPxl()
        self.canvas.unbind("<Button 1>")
        self.process_img()
        
        self.fromSpin.config(state=NORMAL)
        self.fromSpin.delete(0,END)
        self.fromSpin.insert(0,"32")
        self.fromSpin.config(state="readonly")
        
        self.toSpin.config(state=NORMAL)
        self.toSpin.delete(0,END)
        self.toSpin.insert(0,"32")
        self.toSpin.config(state="readonly")
        
        
    def get_narrowContSearchPxl(self):

        for i in range(0,self.radii2.shape[0]):
            for j in range(-10,10):
                self.xCont.append(int(np.round(self.xCenter+self.radii2[i]*np.cos(self.angles2[i])+j*np.cos(self.angles2[i]))))
                self.yCont.append(int(np.round(self.yCenter+self.radii2[i]*np.sin(-self.angles2[i])+j*np.sin(-self.angles2[i]))))                    
#        print (self.xCont, self.yCont)
      
    def extract_contour(self, image, contourImg, num):
        """Call the prostate contouring class and process the img"""
        cont = ProstateContouring(image, self.yCenter, self.xCenter)
        plt.figure()
        plt.imshow(cont.image, cmap=pl.gray())
        plt.show()
        polars = cont.polarFromContourImage(contourImg)     
        cont.readModelShape(polars)
        cont.detectEdges(1) 
        plt.imshow(cont.image, cmap=pl.gray())
        plt.show()
        sigma = 4
        cont.get_narrowContSearchPxl(sigma) 
        plt.imshow(cont.image, cmap=pl.gray())
        plt.show()               
        cont.filterOrientation(np.deg2rad(30))
        plt.imshow(cont.image, cmap=pl.gray())
        plt.show()
        cont.filterContinuity(polars, 7)
        plt.imshow(cont.image, cmap=pl.gray())
        plt.show()
        cont.fillMissingArea()
        plt.imshow(cont.image, cmap=pl.gray())
        plt.show()
        cont.createContour()
        self.contour[...,num] = cont.image
        
        """Build a rgb image with contour in blue on top of original image"""
        rgbImg = np.zeros((self.height, self.width, 3), 'uint8')
        rgbImg[...,0] = image
        rgbImg[...,1] = image
        rgbImg[...,2] = image

        index = np.nonzero(img_as_ubyte(cont.image))
        rgbImg[index[0], index[1], 0] = 0
        rgbImg[index[0], index[1], 1] = 0
        rgbImg[index[0], index[1], 2] = 255
        
        return rgbImg
        
    def process_img(self):
        
        rgbImg = np.zeros((self.height, self.width, 3), 'uint8')
        rgbImg[...,0] = self.imagePNG
        rgbImg[...,1] = self.imagePNG
        rgbImg[...,2] = self.imagePNG
        
        for i in range(-1,2):
            for j in range(-1,2):
                rgbImg[self.yCenter+i, self.xCenter+j, 0] = 255
                rgbImg[self.yCenter+i, self.xCenter+j, 1] = 0
                rgbImg[self.yCenter+i, self.xCenter+j, 2] = 0
    
#        """Get ShapeModel and process the image"""
#        init_contour = skio.imread('contour.png')   
#        rgbImg = self.extract_contour(self.imagePNG, init_contour, 32)
        
        """Convert back the result to PIL image and display in canvas"""
        self.img = Image.fromarray(rgbImg)
        self.displayInCanvas(self.img)
        
        self.message["text"]="Segment the other images by propagating"
        self.button_prop.config(state=NORMAL)
        self.button_modify.config(state=NORMAL)

    def propagateContour(self):
        
        self.nImg = int(self.nSpin.get())
        fromImg = int(self.fromSpin.get())
        toImg = int(self.toSpin.get())
        
        if(not self.isprocessed):
            """Get ShapeModel and process the image"""
            init_contour = skio.imread('contour.png')   
            rgbImg = self.extract_contour(self.imagePNG, init_contour, self.nImg)
            
        for i in range(self.nImg-1,fromImg-1,-1):
            print(i)
            """Read an other image"""
            image = np.asarray(self.dicomFiles.rescaleImg(i))
            
            """Call the prostate contouring class and process the img"""
            rgbImg = self.extract_contour(image, self.contour[...,i+1], i)
            
            self.nSpin.config(state=NORMAL)
            self.nSpin.delete(0,END)
            self.nSpin.insert(0,str(i))
            self.nSpin.config(state="readonly")
        
        for i in range(self.nImg+1,toImg+1):
            print (i)
            
            """Read an other image"""
            image = np.asarray(self.dicomFiles.rescaleImg(i))
            
            """Call the prostate contouring class and process the img"""
            rgbImg = self.extract_contour(image, self.contour[...,i-1], i)
    #                           
            self.nSpin.config(state=NORMAL)
            self.nSpin.delete(0,END)
            self.nSpin.insert(0,str(i))
            self.nSpin.config(state="readonly")
            
        """Convert back the result to PIL image and display in canvas"""
        self.img = Image.fromarray(rgbImg)
        self.displayInCanvas(self.img)
        
        self.message["text"]="Display the 3D volume"
        self.button_3d.config(state=NORMAL)  
        
        self.isprocessed = True
    
    """function to be called when mouse is clicked"""
    def printcoords(self, event):
        #outputting x and y coords to console
        print (event.x,event.y)
        self.xCoor.append(event.x)
        self.yCoor.append(event.y)
        self.canvas.create_line(event.x,event.y,event.x+1, event.y+1,fill="red")
        
    def modifyContour(self):
        self.nImg = int(self.nSpin.get())
        image = np.asarray(self.dicomFiles.rescaleImg(self.nImg))
        self.img = Image.fromarray(image)
        """Convert back the result to PIL image and display in canvas"""    
        self.displayInCanvas(self.img)
        
        self.message["text"]="Draw the new prostate contour"
        self.canvas.bind("<B1-Motion>", self.printcoords)
        
        self.button_stopModifying.config(state=NORMAL)
        
    def stopModifying(self):
        self.canvas.unbind("<B1-Motion>")
        newContour = np.zeros((self.height, self.width),'uint8')
        for i in range(0,len(self.xCoor)):            
            newContour[self.yCoor[i],self.xCoor[i]]=255
            
        self.contour[...,self.nImg] = newContour
        
        
        
        
    def display3D(self):
        fig = plt.figure(figsize=(14,6))
        # `ax` is a 3D-aware axis instance, because of the projection='3d' keyword argument to add_subplot
                
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        ax.set_xlim3d(50,200)
        ax.set_ylim3d(150,250)
        ax.set_zlim3d(0,64)
        
        for i in range(25,41):
            index = np.nonzero(img_as_ubyte(self.contour[...,i]))
            X = index[0]
            Y = index[1]
            Z = np.ones(len(X))*i
            p = ax.scatter(X, Y, zs=Z, s=5)

        plt.show()

#%%
#Instantiate window
fenetre = Tk()
interface = Interface(fenetre)
interface.mainloop()
#interface.destroy()
#fenetre.destroy()