#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 19:59:26 2023

@author: erik
"""

import tkinter as tk
import json
from PIL import Image, ImageTk
from timeline import timeline

# Load map image
eelmap = tk.Tk()
map_img_path = 'lahn2.png'
map_image = Image.open(map_img_path)
# map_img = load_map(map_img_path)
eelmap.geometry("1280x840")  # Set size of root window to 1920x1080 pixels

# Create a PhotoImage object
map_photo = ImageTk.PhotoImage(map_image)
# Create a canvas and add the image to it
canvas = tk.Canvas(eelmap, width=map_image.width, height=map_image.height)
canvas.create_image(0, 0, image=map_photo, anchor=tk.NW)
canvas.pack(fill=tk.BOTH, expand=True)

# define the list of tuples of the coordinates you want the animation to be in
with open("anim_vecs.json", "r", encoding="utf-8") as f:
    coordinates = json.load(f)


# create a dot
dot1 = canvas.create_oval(coordinates[0][0]-3+3,coordinates[0][1]-3+3,coordinates[0][0]+3+3,coordinates[0][1]+3+3, fill='yellow')

# create the second dot with a slight offset
offset = 10
x, y = coordinates[0]
dot2 = canvas.create_oval(x-3, y-3, x+3, y+3, fill='red')

# create a line
x_limit = 760
canvas.create_line(x_limit, 390, x_limit, 440, fill='black')

# define the animation function
def animate_dots():
    global coordinates
    global dot1
    # global dot2
    
    # move the first dot to the next coordinate
    x, y = coordinates.pop(0)
    canvas.coords(dot1, x-3, y-3, x+3, y+3)
    
    # move the second dot with an offset to the next coordinate, if it still exists
    if dot2 in canvas.find_all():
        canvas.coords(dot2, x-3+offset, y-3+offset, x+3+offset, y+3+offset)

    #     # check if the second dot has crossed the line
        if canvas.coords(dot2)[2] <= x_limit:
            # delete the second dot
            canvas.delete(dot2)
            # create a new static dot at the current location of the second dot
            canvas.create_oval(x-3+10, y-3+10, x+3+10, y+3+10, fill='gray')
        
    # if there are still coordinates left, schedule the next move
    if coordinates:
        canvas.after(10, animate_dots)
    

# start the animation after the event loop is started
animate_dots()
# timeline(canvas)
# start the tkinter event loop
eelmap.mainloop()



