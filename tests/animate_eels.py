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
from move_points import Location
import json

conn = sqlite3.connect('mydatabase.db')

with open("locations.json", "r", encoding="utf-8") as f:
    loc_coords = json.load(f)

# Get the unique location names in the correct order
locations_order = ['LÖHN_OW','LÖHN_UW','WEIL_OW','WEIL_UW','KIRS_OW',
                      'KIRS_UW','FÜRF_OW','FÜRF_UW','VILL_OW','VILL_UW',
                      'RUNK_OW','RUNK_UW','LIMB_OW','LIMB_UW','DIEZ_OW',
                      'DIEZ_UW','CRAM_OW','CRAM_UW','KALK_OW','KALK_UW']


def time_differences(conn, loc_in_order):
    """calculates the time differences between different locations and the 
    stationary time periods and stores them in a list of tuples"""
    
    cursor = conn.cursor()
    rangequery = "SELECT ID_HEX, Ort, Min(Serial_XLDate) AS min_date, MAX(Serial_XLDate) AS max_date FROM eeltable GROUP BY ID_HEX, Ort"
    
    # execute the query and store the results in a list
    rows = cursor.execute(rangequery).fetchall()    
    # create a list to store the time differences for each eel at each location
    time_diffs = []
    time_diffs_check = []
    
    # sort the rows by location so that they appear in the same order as locations_in_order
    rows = sorted(rows, key=lambda row: (row[0], loc_in_order.index(row[1])))
    
    stationary_phases =[]
    
    for row in rows:
        ID_HEX = row[0]
        location = row[1]
        stationary_time = row[3]-row[2]
        stationary_phases.append((ID_HEX,location,stationary_time))
    
    # loop through the rows and calculate the time differences
    for i in range(len(rows)-1):
        # get the current row and the next row in the list
        row1 = rows[i]
        row2 = rows[i+1]
    
        # if the two rows have the same ID_HEX and different locations, calculate the time difference
        if row1[0] == row2[0] and row1[1] != row2[1]:
            # calculate the time difference between the two rows
            diff = row2[2] - row1[3]
    
            # get the ID_HEX and location for the current row
            ID_HEX = row1[0]
            location1 = row1[1]
            location2 = row2[1]
            
            if diff > 0 and diff < 365:
                # add the time difference to the list
                time_diffs.append((ID_HEX, location1, location2, diff))
            else:
                time_diffs_check.append((ID_HEX,location1,location2,diff))
    
    return time_diffs,time_diffs_check,stationary_phases


time_diffs,time_diffs_check,stationary_time = time_differences(conn,locations_order)

def calc_velocities(time_differences, loc_coords, locations_order):
    # Create empty lists to store information
    ID_HEX_list = []
    loc1_list = []
    loc2_list = []
    vector_list = []
    vec_dist_list = []
    velo_norm_list = []

    
    for loc_pair in time_differences:
        ID_HEX, loc1, loc2, time_diff = loc_pair
        
        # Determine the vector tuple for the movement
        veclist = []
        loc1_idx = locations_order.index(loc1)
        loc2_idx = locations_order.index(loc2)
        loc1 = loc_coords[loc1]
        loc2 = loc_coords[loc2]
        
        for i in range(loc1_idx, loc2_idx):
            cur_loc = loc_coords[locations_order[i]]
            next_loc = loc_coords[locations_order[i+1]]
            x1, y1 = cur_loc
            x2, y2 = next_loc
            dx = x2 - x1
            dy = y2 - y1
            vector = (dx, dy)
            veclist.append(vector)
            vec_dist = 0
            
        # Calculate the velocity for all vectors in the list
        vec_dist = sum(math.sqrt(vec[0]**2 + vec[1]**2) for vec in veclist)
        velo_norm = int((math.log(vec_dist / time_diff + 1)) * 100)

        # Append information to lists
        ID_HEX_list.append(ID_HEX)
        loc1_list.append(loc1)
        loc2_list.append(loc2)
        vector_list.append(veclist)
        vec_dist_list.append(vec_dist)
        velo_norm_list.append(velo_norm)
            
    # Create dataframe from lists
    df = pd.DataFrame({
        'ID_HEX': ID_HEX_list,
        'loc1': loc1_list,
        'loc2': loc2_list,
        'vector': vector_list,
        'vec_dist': vec_dist_list,
        'velo_norm': velo_norm_list
    })
    
    return df



df = calc_velocities(time_diffs, loc_coords, locations_order)


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

animate(canvas, df)

# for key, coords in loc_coords.items():
#     canvas.create_oval(coords[0]-5, coords[1]-5, coords[0]+5, coords[1]+5)

eelmap.mainloop()