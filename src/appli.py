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

"""Create a class
"""
class Interface(Frame):
    
    """class which is derived from a window
    """
    
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        self.nb_clic = 0
        
        #Build widgets
        self.message = Label(self, text="You didn't click on the button")
        self.message.pack()
        
        self.button_exit = Button(self, text="Exit", command=self.quit)
        self.button_exit.pack(side="left")
        
        self.button_click = Button(self, text="Click here", fg="red",
                                   command=self.cliquer)
        self.button_click.pack(side="right")
        
    
    def cliquer(self):
        """there was a click on the button
        we change the value  of the label message"""
        self.nb_clic += 1
        self.message["text"] = "You have clicked {} times".format(self.nb_clic)
    
def selectImage(fenetre):
    File = askopenfilename(parent=fenetre, initialdir="C:/",title='Choose an image.')
    img = ImageTk.PhotoImage(Image.open(File))
    return img
    
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

"""
Display 17th image
"""
k = 17
im = DS[k].pixel_array
im = img_as_float(im)
io.imsave("prostate3.png", im)

#instantiate label
#champ_label = Label(fenetre, text="Salut")
#champ_label.pack()
##
#button_exit = Button(fenetre, text="Quitter", command=fenetre.quit)
##display label in the window
#
#button_exit.pack()
#
###Start Tkinter loop which interrup when we close the window
#fenetre.mainloop()
#fenetre.destroy()

#%%
#Instantiate window
#fenetre = Tk()
#interface = Interface(fenetre)
#interface.mainloop()
#interface.destroy()
#fenetre.destroy()

"""read image in canvas
move later on to class"""

fenetre2 = Tk()
button_exit = Button(fenetre2, text="Exit", command=fenetre2.quit)
button_exit.pack(side='right')

button_open = Button(fenetre2, text="Open", command=0)
button_open.pack(side='left')

frame = Frame(fenetre2, bd=2, relief=SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
xscroll = Scrollbar(frame, orient=HORIZONTAL)
xscroll.grid(row=1, column=0, sticky=E+W)
yscroll = Scrollbar(frame)
yscroll.grid(row=0, column=1, sticky=N+S)
canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
xscroll.config(command=canvas.xview)
yscroll.config(command=canvas.yview)
frame.pack(fill=BOTH, expand=1)

File = askopenfilename(parent=fenetre2, initialdir="C:/",title='Choose an image.')
img = ImageTk.PhotoImage(Image.open(File))
canvas.create_image(0,0,image=img,anchor="nw")
canvas.config(scrollregion=canvas.bbox(ALL))

fenetre2.mainloop()
fenetre2.destroy()