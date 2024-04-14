# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:36:13 2023

@author: TheRickestRick
"""
import pandas as pd
# import numpy as np

import tkinter as tk
from PIL import Image,ImageTk
# import math
from animate_eels_3 import df
# import datetime as dt
import json
from timeline import timeline
import random
import threading

# # Load map image
# eelmap = tk.Tk()
# map_img_path = 'lahn2.png'
# map_image = Image.open(map_img_path)
# # map_img = load_map(map_img_path)
# eelmap.geometry("1280x840")  # Set size of root window to 1920x1080 pixels

# # Create a PhotoImage object
# map_photo = ImageTk.PhotoImage(map_image)
# # Create a canvas and add the image to it

# canvas = tk.Canvas(eelmap, width=map_image.width, height=map_image.height)
# canvas.create_image(0, 0, image=map_photo, anchor=tk.NW)
# canvas.pack(fill=tk.BOTH, expand=True)


eelmap = tk.Tk()
eelmap.geometry("1280x840")  # Set size of root window to 1920x1080 pixels
canvas = tk.Canvas(eelmap,width = 1280,height = 840 )
canvas.pack(fill=tk.BOTH, expand=True)

# define the list of tuples of the coordinates you want the animation to be in
with open("anim_vecs.json", "r", encoding="utf-8") as f:
    coordinates = json.load(f)
coordinates = [tuple(map(int, sublist)) for sublist in coordinates] 

# # create a line
x_limit = 760
canvas.create_line(x_limit, 390, x_limit, 440, fill='black')


# define a function that moves a dot along a path
def move_dot(dot, coordinates):
    # move the dot along the path
    for x, y in coordinates:
        canvas.coords(dot, x-3, y-3, x+3, y+3)
        if canvas.coords(dot)[0] <= x_limit:
            # create a new static dot at the current location of the moving dot
            canvas.create_oval(x-3, y-3, x+3, y+3, fill='gray')
            break
        canvas.after(10)
    # delete the dot when it reaches the end of the path
    canvas.delete(dot)

# create multiple dots and move them along the path using threading
threads = []
for i in range(5):
    # create a dot at a random position
    x, y = random.choice(coordinates)
    dot = canvas.create_oval(x-3, y-3, x+3, y+3, fill='yellow')
    # create a thread to move the dot along the path
    thread = threading.Thread(target=move_dot, args=(dot, coordinates))
    threads.append(thread)
    thread.start()

# wait for all threads to finish
for thread in threads:
    thread.join() 

# timeline(canvas)
# start the tkinter event loop
eelmap.mainloop()