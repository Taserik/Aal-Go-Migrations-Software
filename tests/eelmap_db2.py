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

def calc_distances(locations):
    """
    Calculates the distances between all pairs of locations in the list `locations`.
    """
    distances = []
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            loc1, x1, y1 = locations[i]
            loc2, x2, y2 = locations[j]
            if j == i+1:
                # locations are adjacent
                distance = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                distances.append((loc1, loc2, distance))
            else:
                # locations are not adjacent, need to add up distances
                locs_between = locations[i:j]
                total_distance = 0
                for k in range(len(locs_between)):
                    loc3, x3, y3 = locs_between[k]
                    loc4, x4, y4 = locs_between[k+1] if k+1 < len(locs_between) else (loc2, x2, y2)
                    segment_distance = int(((x4 - x3)**2 + (y4 - y3)**2)**0.5)
                    total_distance += segment_distance
                distances.append((loc1, loc2, total_distance))
    return distances


distances = calc_distances(loc_coordinates)

def get_vector(loc_coordinates):
    """
    Returns a dictionary of vectors between adjacent locations.
    """
    vectors = {}
    for i in range(len(loc_coordinates)-1):
        loc1 = loc_coordinates[i]
        loc2 = loc_coordinates[i+1]
        
        x1, y1 = loc1[1:]
        x2, y2 = loc2[1:]
        dx = x2 - x1
        dy = y2 - y1
        vectors[(loc1[0], loc2[0])] = (dx, dy)
    
    return vectors



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


vector_dict = get_vector(loc_coordinates)
time_diffs,time_diffs_check,stationary_time = time_differences(conn,locations_order)


def calc_velocities(time_differences, loc_coordinates):
    distances = calc_distances(loc_coordinates)
    # vectors = get_vector(loc_coordinates)
    velocities = []
    
    for loc_pair in time_differences:
        ID_HEX, loc1, loc2, time_diff = loc_pair
        
        # Calculate the velocity
        dist = [d[2] for d in distances if d[:2] == (loc1, loc2)][0]
        velo = dist / time_diff
        velo_norm = (math.log(velo + 1) / math.log(max(velocities) + 1)) * 100
        loc1 = loc_coords[loc1]
        loc2 = loc_coords[loc2]
        
        # Get the vector
        # vector = vectors[(loc1, loc2)]
        velocities.append((ID_HEX,loc1,loc2, velo_norm))

    return velocities

import math




def get_movement_vectors(time_diffs, loc_coordinates, vector_dict, locations_order):
    movement_vectors = []

    for time_diff in time_diffs:
        ID_HEX, loc1, loc2, time_diff = time_diff
        
        # Determine the vector tuple for the movement
        vectors = []
        loc1_idx = locations_order.index(loc1)
        loc2_idx = locations_order.index(loc2)
        if loc1_idx < loc2_idx:
            for i in range(loc1_idx, loc2_idx):
                cur_loc = locations_order[i]
                next_loc = locations_order[i+1]
                vector_key = (cur_loc, next_loc)
                vectors.append(vector_dict[vector_key])
        else:
            for i in range(loc2_idx, loc1_idx):
                cur_loc = locations_order[i]
                next_loc = locations_order[i+1]
                vector_key = (cur_loc, next_loc)
                vectors.append(vector_dict[vector_key][::-1])
            vectors.reverse()
        
        movement_vectors.append(tuple(vectors))
    
    return movement_vectors



vectors = get_movement_vectors(time_diffs,loc_coordinates,vector_dict,locations_order)


velo = calc_velocities(time_diffs,loc_coordinates)

velovec = [vec + vectors[i] for i, vec in enumerate(velo)]

import time
import numpy as np

# def animate_eels(canvas, eel_data, loc_coordinates, delay):
#     """Animates eels moving along the given vectors on the map."""
    
#     # Initialize the previous eel ID to None
#     prev_eel_id = None
    
#     # Loop through the list of eel_data tuples
#     for eel in eel_data:
        
#         # Get the ID_HEX of the eel
#         eel_id = eel[0]
        
#         # Check if this is a new eel or not
#         if eel_id != prev_eel_id:
#             # Get the starting location of the eel
#             loc1 = eel[1]
#             x, y = loc_coordinates[loc1]
#             # Create a new dot for the eel on the canvas
#             radius = 5
#             fill_color = 'green'
#             dot = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill_color)
        
#         # Loop through the vectors for the eel
#         for vector in eel[4:]:
#             # Extract the vector information
#             x_vel, y_vel = vector
#             distance = np.sqrt(x_vel**2 + y_vel**2)
#             duration = distance / eel[3]
#             # Calculate the destination coordinates of the dot
#             dest_x = x + x_vel
#             dest_y = y + y_vel
#             # Animate the dot moving along the vector
#             steps = int(duration * 1000 / delay)
#             for i in range(steps):
#                 delta_x = (dest_x - x) / steps
#                 delta_y = (dest_y - y) / steps
#                 x += delta_x
#                 y += delta_y
#                 canvas.coords(dot, x - radius, y - radius, x + radius, y + radius)
#                 canvas.update()
#                 time.sleep(delay / 1000)
#             # Update the current position of the dot
#             x, y = dest_x, dest_y
        
#         # Update the previous eel ID
#         prev_eel_id = eel_id

# import threading

# def animate_eels(canvas, eel_data, loc_coordinates, delay):
#     """Animates eels moving along the given vectors on the map."""
    
#     # Normalize the velocities for each eel
#     for i, eel in enumerate(velovec):
#         velocity = np.array([eel[4][0], eel[4][1]])
#         norm = np.linalg.norm(velocity)
#         if norm != 0:
#             norm_velocity = tuple(velocity / norm)
#             velovec[i] = (eel[0], eel[1], eel[2], eel[3], norm_velocity)


# animate_eels(canvas,velovec, loc_coords, 1000)

class Eel:
    def __init__(self, canvas, velovec):
        self.canvas = canvas
        self.velovec = velovec
        self.radius = 5
        self.dots = {}
        self.colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta']
        self.dot_count = 0
        
        # start animation
        self.draw()
    
    def draw(self):
        for i in range(len(self.velovec)):
            id_hex, start, end, velocity, *vectors = self.velovec[i]
            if id_hex not in self.dots:
                # create a new dot if this is the first time seeing this ID_HEX
                fill_color = self.colors[self.dot_count % len(self.colors)]
                dot = self.canvas.create_oval(start[0] - self.radius, start[1] - self.radius, 
                                              start[0] + self.radius, start[1] + self.radius, 
                                              fill=fill_color)
                self.dots[id_hex] = {'dot': dot, 'vector_idx': 0}
                self.dot_count += 1
            else:
                # move the existing dot to its new location along the specified vectors
                dot = self.dots[id_hex]['dot']
                vector_idx = self.dots[id_hex]['vector_idx']
                vector = vectors[vector_idx]
                dx, dy = vector
                new_coords = self.canvas.coords(dot)[0:2]
                new_coords[0] += dx * velocity / 100
                new_coords[1] += dy * velocity / 100
                self.canvas.coords(dot, new_coords[0] - self.radius, new_coords[1] - self.radius, 
                                    new_coords[0] + self.radius, new_coords[1] + self.radius)
                
                # check if the dot has reached the end location
                if new_coords[0] >= end[0] and new_coords[1] >= end[1]:
                    # move to the next vector and reset the location to the end location
                    self.dots[id_hex]['vector_idx'] = (vector_idx + 1) % len(vectors)
                    self.canvas.coords(dot, end[0] - self.radius, end[1] - self.radius, 
                                        end[0] + self.radius, end[1] + self.radius)

class EelMap:
    def __init__(self, master, velovec):
        self.master = master
        self.canvas = master
        self.eels = []
        for v in velovec:
           vx, vy = v[4]
           x, y = v[1]
           eel = Eel(self.canvas, velovec)
           self.eels.append(eel)
           eel.draw()

    def animate_eels(self):
        for eel in self.eels:
            eel.move()
        self.canvas.delete("all")
        for eel in self.eels:
            eel.draw()
        self.master.after(50, self.animate_eels)


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
app = EelMap(canvas, velovec)

canvas.after(50, app.animate_eels)
eelmap.mainloop()




time_diffs,time_diffs_check,stationary_time = time_differences(conn,locations_order)
    
conn.close()
# eelmap.mainloop()
