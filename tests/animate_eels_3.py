#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 00:42:11 2023

@author: erik
"""
import pandas as pd
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import math
import time
import numpy as np
# from move_points import Location
import json

conn = sqlite3.connect('mydatabase.db')

with open("locations.json", "r", encoding="utf-8") as f:
    loc_coords = json.load(f)

# Get the unique location names in the correct order
locations_order = ['LÖHN_OW','LÖHN_UW','WEIL_OW','WEIL_UW','KIRS_OW',
                      'KIRS_UW','FÜRF_OW','FÜRF_UW','VILL_OW','VILL_UW',
                      'RUNK_OW','RUNK_UW','LIMB_OW','LIMB_UW','DIEZ_OW',
                      'DIEZ_UW','CRAM_OW','CRAM_UW','KALK_OW','KALK_UW']



    


    

def animate(canvas, df):
    # get the first row of each ID_HEX
    id_hex_list = df['ID_HEX'].unique()
    first_rows = [df[df['ID_HEX']==id_hex].iloc[0] for id_hex in id_hex_list]

    # create a dot for each first row
    dots = []
    for row in first_rows:
        loc = row['loc1']
        dot = canvas.create_oval(loc[0]-5, loc[1]-5, loc[0]+5, loc[1]+5, fill="red")
        dots.append(dot)

    # loop over the rows of the dataframe
    for idx, row in df.iterrows():
        id_hex = row['ID_HEX']
        loc1 = row['loc1']
        vectors = row['vector']
        velo_norm = row['velo_norm']
        dist = row['vec_dist']
        
        # find the dot corresponding to this row's ID_HEX
        dot_idx = id_hex_list.tolist().index(id_hex)
        dot = dots[dot_idx]

        # loop over the vectors and move the dot accordingly
        current_loc = loc1
        for vec in vectors:
            # calculate time to move
            time_to_move = dist / velo_norm

            # calculate the new position of the dot
            new_pos = (current_loc[0]+vec[0], current_loc[1]+vec[1])

            # move the dot to the new position
            canvas.coords(dot, new_pos[0]-5, new_pos[1]-5, new_pos[0]+5, new_pos[1]+5)
            canvas.update()
            
            time.sleep(0.1)
            canvas.update()

            # update current location
            current_loc = new_pos


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

# locations = Location(canvas, loc_coords)

# animate(canvas, df)

# for key, coords in loc_coords.items():
#     canvas.create_oval(coords[0]-5, coords[1]-5, coords[0]+5, coords[1]+5)

eelmap.mainloop()