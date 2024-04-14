#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 09:53:27 2023

@author: erik
"""
import pandas as pd
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import math
import time
import numpy as np

# Create a connection to the SQLite database
conn = sqlite3.connect('mydatabase.db')


# # Load map image
# eelmap = tk.Tk()
# map_img_path = 'lahn.png'
# map_image = Image.open(map_img_path)
# # map_img = load_map(map_img_path)
# eelmap.geometry("1920x1080")  # Set size of root window to 1920x1080 pixels

# # Create a PhotoImage object
# map_photo = ImageTk.PhotoImage(map_image)
# # Create a canvas and add the image to it
# canvas = tk.Canvas(eelmap, width=map_image.width, height=map_image.height)
# canvas.create_image(0, 0, image=map_photo, anchor=tk.NW)
# # canvas.image_reference = canvas.image # Keep a reference to the PhotoImage object
# canvas.pack(fill=tk.BOTH, expand=True)


# Get the unique location names in the correct order
locations_order = ['LÖHN_OW','LÖHN_UW','WEIL_OW','WEIL_UW','KIRS_OW',
                      'KIRS_UW','FÜRF_OW','FÜRF_UW','VILL_OW','VILL_UW',
                      'RUNK_OW','RUNK_UW','LIMB_OW','LIMB_UW','DIEZ_OW',
                      'DIEZ_UW','CRAM_OW','CRAM_UW','KALK_OW','KALK_UW']

loc_coordinates = [('LÖHN_OW',1340, 35), ('LÖHN_UW',1300, 100), ('WEIL_OW',1308, 140), ('WEIL_UW',1275, 155), 
            ('KIRS_OW',1225, 215), ('KIRS_UW',1230, 260), ('FÜRF_OW',1250, 395), ('FÜRF_UW',1255, 440), 
            ('VILL_OW',1075, 550), ('VILL_UW',1070, 580), ('RUNK_OW',1000,540), ('RUNK_UW',950,540), 
            ('LIMB_OW',810,570), ('LIMB_UW',690,570), ('DIEZ_OW',535,640), ('DIEZ_UW',550,685), 
            ('CRAM_OW',305,815), ('CRAM_UW',340,840), ('KALK_OW',258,950), ('KALK_UW',225,925)]

loc_coords = {'LÖHN_OW': (1340, 35), 'LÖHN_UW': (1300, 100), 'WEIL_OW': (1308, 140), 'WEIL_UW': (1275, 155), 
            'KIRS_OW': (1225, 215), 'KIRS_UW': (1230, 260), 'FÜRF_OW': (1250, 395), 'FÜRF_UW': (1255, 440), 
            'VILL_OW': (1075, 550), 'VILL_UW': (1070, 580), 'RUNK_OW': (1000,540), 'RUNK_UW': (950,540), 
            'LIMB_OW': (810,570), 'LIMB_UW': (690,570), 'DIEZ_OW': (535,640), 'DIEZ_UW': (550,685), 
            'CRAM_OW': (305,815), 'CRAM_UW': (340,840), 'KALK_OW': (258,950), 'KALK_UW': (225,925)}


def time_differences(conn, loc_in_order):
    """calculates the time differences between different locations and the 
    stationary time periods and stores them in a list of tuples"""
    
    cursor = conn.cursor()
    rangequery = "SELECT * FROM eeltable GROUP BY ID_HEX, Ort"
    
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
    # vectors = get_vector(loc_coordinates)
    velocities = []
    vector_list = []
    
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
            # vectorlist.reverse()
            vec_dist = 0
        for e in range(len(veclist)):
            # Calculate the velocity
            vec_dist += (math.sqrt(veclist[e][0]**2 + veclist[e][1]**2))
        # berechne Geschwindigkeit und logarhytmire diese
        velo_norm = int((math.log(vec_dist / time_diff + 1)) * 100)
        
        velocities.append(velo_norm)
        vector_list.append((ID_HEX,loc1,loc2,veclist))

    return velocities, vector_list
velocities,vector_list = calc_velocities(time_diffs, loc_coords, locations_order)

tup_total = vector_list[0]
move_list = []
for i in range(len(vector_list)-1):
    tup1 = vector_list[i][0]
    tup2 = vector_list[i+1][0]
    if tup1 != tup2:
        move_list.append(tup_total)
        tup_total = vector_list[i+1]
    else:
        tup_total += vector_list[i+1][3:]


class Eel:
    def __init__(self, canvas, velovec):
        self.canvas = canvas
        self.velovec = velovec
        self.radius = 5
        self.dots = {}
        self.dot_coords = {}
        self.colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta']
        self.dot_count = 0
        
        # start animation
        self.draw()        
        self.new_coords()
        
    def draw(self):
        for j in range(len(self.velovec)):
            id_hex, start, end, *vectors = self.velovec[j]
            # create a new dot if this is the first time seeing this ID_HEX
            fill_color = self.colors[self.dot_count % len(self.colors)]
            dot = self.canvas.create_oval(start[0] - self.radius, start[1] - self.radius, 
                                          start[0] + self.radius, start[1] + self.radius, 
                                          fill=fill_color)
            self.dots[id_hex] = {'dot': dot, 'vector_idx': 0}
            self.dot_count += 1
                
    def new_coords(self):
        for i in range(len(self.velovec)):
            id_hex, start, end, velocity, *vectors = self.velovec[i]
            # move the existing dot to its new location along the specified vectors
            dot = self.dots[id_hex]['dot']
            for e in range(len(vectors[i])):
                
                vector = vectors[i][e]
                dx, dy = vector
                # x,y = start
                # new_coords_x = x + dx
                # new_coords_y = y + dy
                new_coords = self.canvas.coords(dot)[0:2]
                new_coords[0] += dx
                new_coords[1] += dy
                
                
                self.canvas.coords(dot, new_coords[0] - self.radius, new_coords[1] - self.radius, 
                                new_coords[0] + self.radius, new_coords[1] + self.radius)
                # vector_idx = self.dots[id_hex]['vector_idx']

                
                # check if the dot has reached the end location
                if new_coords[0] >= end[0] and new_coords[1] >= end[1]:
                    # move to the next vector and reset the location to the end location
                    # self.dots[id_hex]['vector_idx'] = (vector_idx + 1) % len(vectors)
                    self.canvas.coords(dot, end[0] - self.radius, end[1] - self.radius, 
                                        end[0] + self.radius, end[1] + self.radius)
    #     # self.canvas.after(1000,self.move())             


# Load map image
eelmap = tk.Tk()
map_img_path = 'lahn.png'
map_image = Image.open(map_img_path)
# map_img = load_map(map_img_path)
eelmap.geometry("1920x1080")  # Set size of root window to 1920x1080 pixels

# Create a PhotoImage object
map_photo = ImageTk.PhotoImage(map_image)
# Create a canvas and add the image to it
canvas = tk.Canvas(eelmap, width=map_image.width, height=map_image.height)
canvas.create_image(0, 0, image=map_photo, anchor=tk.NW)
canvas.pack(fill=tk.BOTH, expand=True)
app = Eel(canvas, move_list)

# canvas.after(50, app.animate_eels)
eelmap.mainloop()




time_diffs,time_diffs_check,stationary_time = time_differences(conn,locations_order)
    
conn.close()
# eelmap.mainloop()
