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
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

import dicom
import os
import numpy as np

from skimage import img_as_float
from skimage import io

        
"""Create a class"""
class Interface(Frame):
    
    """class which is derived from a frame"""
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        self.nb_clic = 0
        #Coordinates of pxl representing the contour
        self.xCoor = []
        self.yCoor = []
        #Coordinates of the prostate center
        self.xCenter = 0
        self.yCenter = 0
        #List of computed angles and radius from center
        self.angles = []
        self.radii = []
        #Coordinates of pxl inside narrow contour search
        self.xCont = []
        self.yCont = []
        
        #Build widgets
        self.message = Label(self,        self.button_open = Button(self, text="Open", fg="blue", 
 text="Open an image")
        self.message.pack()
                
        self.button_click = Button(self, text="Draw contour", fg="red",
                                   command=self.cliquer)
        self.button_click.pack(side="right")
        
        self.button_stop = Button(self, text="Stop contour", command=self.stop_click)
        self.button_stop.pack(side="right")
        
                                  command=self.openImg)
        self.button_open.pack(side="left")
        
        self.button_center = Button(self, text="Click center", fg="red",
                                    command=self.click_center)
        self.button_center.pack(side="right")
       
        self.frame = Frame(self, bd=2, relief=SUNKEN)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.xscroll = Scrollbar(self.frame, orient=HORIZONTAL)
        self.xscroll.grid(row=1, column=0, sticky=E+W)
        self.yscroll = Scrollbar(self.frame)
        self.yscroll.grid(row=0, column=1, sticky=N+S)
        self.canvas = Canvas(self.frame, bd=0, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        self.canvas.grid(row=0, column=0, sticky=N+S+E+W)
        self.xscroll.config(command=self.canvas.xview)
        self.yscroll.config(command=self.canvas.yview)
        self.frame.pack(fill=BOTH, expand=1)

        
        """function to be called when mouse is clicked"""
    def printcoords(self, event):
        #outputting x and y coords to console
        print (event.x,event.y)
        self.xCoor.append(event.x)
        self.yCoor.append(event.y)
        self.canvas.create_line(event.x,event.y,event.x+1, event.y+1,fill="red")
#        self.canvas.bind("<Motion>", self.updateTracking)
        
    def getCenter(self, event):
        self.xCenter = event.x
        self.yCenter = event.y
        self.compute_anglesAndRadii()
        self.get_narrowContSearchPxl()
        self.process_img()
#        for i in range(0,len(self.xCoor)-1):
#            self.angles.append( np.arctan2(self.yCoor[i]-self.yCenter, self.xCoor[i]-self.xCenter) )
#            self.radii.append( np.sqrt((self.yCoor[i]-self.yCenter)**2 + (self.xCoor[i]-self.xCenter)**2 ))
#        print (self.angles, self.radii)
        
    def compute_anglesAndRadii(self):
        for i in range(0,len(self.xCoor)-1):
            self.angles.append( np.arctan2(self.yCoor[i]-self.yCenter, self.xCoor[i]-self.xCenter) )
            self.radii.append( np.sqrt((self.yCoor[i]-self.yCenter)**2 + (self.xCoor[i]-self.xCenter)**2 ))
        print (self.angles, self.radii)
        
    def get_narrowContSearchPxl(self):
        for i in range(0,len(self.radii)):
            for j in range(-10,10):
                self.xCont.append(int(np.round(self.xCenter+self.radii[i]*np.cos(self.angles[i])+j*np.cos(self.angles[i]))))
                self.yCont.append(int(np.round(self.yCenter+self.radii[i]*np.sin(self.angles[i])+j*np.sin(self.angles[i]))))
            
#        print (self.xCont, self.yCont)
        
    def process_img(self):
#        self.pixels = list(self.img.getdata())
#        width, height = self.img.size
#        self.pixels = [self.pixels[i * width:(i + 1) * width] for i in range(1,height)]
#        for i in range(self.xCenter, self.xCenter+100):
#            for row in self.pixels:
#                row[i] = 0
        #Convert to array and Test removing pixels
        self.pixels = np.asarray(self.img.getdata(), np.uint16)
        width, height = self.img.size
        self.pixels = np.reshape(self.pixels, (height, width), order='A')
        for i in range(self.xCenter,self.xCenter+100):
            for j in range(self.yCenter,self.yCenter+100):
                self.pixels[i,j]=0

        #Convert to Image and display in canvas
        self.img_proc = Image.new(self.img.mode, self.img.size)
#        self.img_proc.putdata(self.pixels)
#        self.imgtk = ImageTk.PhotoImage(self.img_proc)

        #Remove pixels directly from Image
        for i in range(self.xCenter,self.xCenter+100):
            for j in range(self.yCenter,self.yCenter+100):
                self.img.putpixel((i,j),0)
        
        for i in range(0,len(self.xCont)):
            self.img_proc.putpixel((self.xCont[i],self.yCont[i]),self.img.getpixel((self.xCont[i],self.yCont[i])))
        
                
        self.imgtk = ImageTk.PhotoImage(self.img_proc)
        self.canvas.create_image(0,0,image=self.imgtk,anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
#        io.imsave("pxlRemovedArray.png", self.pixels)
        
    def openImg(self):
        #open image and display in canvas
        File = askopenfilename(parent=fenetre, initialdir="C:/",title='Choose an image.')
        self.img = Image.open(File)
        self.imgtk = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0,0,image=self.imgtk,anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))
        self.message["text"]="Now press on click center do draw the prostate shape"
        
    def cliquer(self):
        """there was a click on the button
        we change the value  of the label message"""
        #mouseclick event
        self.message["text"]="Draw the prostate contour"
        self.canvas.bind("<B1-Motion>", self.printcoords)
        
    def stop_click(self):
#        self.canvas.unbind("<Button 1>") #use returned variable of bind fct as 2nd param if unbind only one fct 
        self.canvas.unbind("<B1-Motion>")
        print (self.xCoor[len(self.xCoor)-1])

    
    def click_center(self):
        self.canvas.bind("<Button 1>", self.getCenter)
    

#%%
#Instantiate window
fenetre = Tk()
interface = Interface(fenetre)
interface.mainloop()
#interface.destroy()
#fenetre.destroy()