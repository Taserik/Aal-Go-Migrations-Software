#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 15:31:36 2023

@author: erik
"""

import numpy as np
import json
import math


# Load coordinates from file
with open("set_locs.json", "r", encoding="utf-8") as f:
    set_locs = json.load(f)

# Create a list of coordinate tuples
coordinates = [(coord[0], coord[1]) for coord in set_locs.values()]

# Define the desired segment length
segment_length = 3

# Create a new list of coordinates with the desired segment length
anim_locs = [coordinates[0]]

for i in range(1, len(coordinates)):
    # Get the vector between the current and previous coordinate
    vector = np.array(coordinates[i]) - np.array(coordinates[i-1])
    
    # Calculate the length of the vector
    vector_length = np.linalg.norm(vector)
    
    # Calculate the number of segments needed to achieve the desired segment length
    num_segments = int(np.ceil(vector_length / segment_length))
    
    # Calculate the increment for each segment
    increment = vector / num_segments
    
    # Add the new coordinates to the list
    for k in range(num_segments):
        new_coord = tuple(np.array(coordinates[i-1]) + k * increment)
        anim_locs.append(new_coord)
anim_locs = [tuple(int(x) for x in vec) for vec in anim_locs]

# Save the new list of coordinates as a JSON file
with open("anim_locs.json", "w", encoding="utf-8") as f:
    json.dump(anim_locs, f, ensure_ascii=False)

# Load coordinates from file
with open("locations.json", "r", encoding="utf-8") as f:
    loc_coords = json.load(f)
    
closest_indexes = {}

def find_closest_index(target, points):
    closest_dist = float('inf')
    closest_index = None
    for i, point in enumerate(points):
        dist = math.sqrt((target[0]-point[0])**2 + (target[1]-point[1])**2)
        if dist < closest_dist:
            closest_dist = dist
            closest_index = i
    return closest_index

for loc, coords in loc_coords.items():
    closest_index = find_closest_index(coords, anim_locs)
    # print(f"Closest tuple to location {loc} is {anim_locs[closest_index]} at index {closest_index}")
    closest_indexes[loc] = closest_index

path_dict= {}

# Loop over the keys in the closest_indexes dictionary
for start_loc in closest_indexes.keys():
    # Loop over the keys again, starting from the next key
    for end_loc in list(closest_indexes.keys())[list(closest_indexes.keys()).index(start_loc) + 1:]:
        # Create the key for the new dictionary entry
        path_key = start_loc + ',' + end_loc
        # Create the slice of anim_locs
        start_idx = closest_indexes[start_loc]
        end_idx = closest_indexes[end_loc] + 1
        path_slice = anim_locs[start_idx:end_idx]
        # Add the new entry to the path dictionary
        path_dict[path_key] = path_slice
    
# Save the new list of coordinates as a JSON file
with open("path_dict.json", "w", encoding="utf-8") as f:
    json.dump(path_dict, f, ensure_ascii=False)
