# -*- coding: utf-8 -*-
"""
Created on Thu May  5 10:23:36 2016

@author: Yanik
"""

#%%
"""Import libraries
"""
#import numpy as np
from tkinter import * #Change for Tkinter if python 2
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

#%%
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

#function to be called when mouse is clicked
def printcoords(event):
    #outputting x and y coords to console
    print (event.x,event.y)
#mouseclick event
canvas.bind("<Button 1>",printcoords)

fenetre2.mainloop()
fenetre2.destroy()