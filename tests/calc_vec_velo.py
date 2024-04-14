#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 11:40:30 2023

@author: erik
"""

import sqlite3
import math
import pandas as pd
import numpy as np

conn = sqlite3.connect('mydatabase.db')


# Get the unique location names in the correct order
locations_order = ['LÖHN_OW','LÖHN_UW','WEIL_OW','WEIL_UW','KIRS_OW',
                      'KIRS_UW','FÜRF_OW','FÜRF_UW','VILL_OW','VILL_UW',
                      'RUNK_OW','RUNK_UW','LIMB_OW','LIMB_UW','DIEZ_OW',
                      'DIEZ_UW','CRAM_OW','CRAM_UW','KALK_OW','KALK_UW']

# loc_coordinates = [('LÖHN_OW',1340, 35), ('LÖHN_UW',1300, 100), ('WEIL_OW',1308, 140), ('WEIL_UW',1275, 155), 
#             ('KIRS_OW',1225, 215), ('KIRS_UW',1230, 260), ('FÜRF_OW',1250, 395), ('FÜRF_UW',1255, 440), 
#             ('VILL_OW',1075, 550), ('VILL_UW',1070, 580), ('RUNK_OW',1000,540), ('RUNK_UW',950,540), 
#             ('LIMB_OW',810,570), ('LIMB_UW',690,570), ('DIEZ_OW',535,640), ('DIEZ_UW',550,685), 
#             ('CRAM_OW',305,815), ('CRAM_UW',340,840), ('KALK_OW',258,950), ('KALK_UW',225,925)]

loc_coords = {'LÖHN_OW': (1340, 35), 'LÖHN_UW': (1300, 100), 'WEIL_OW': (1308, 140), 'WEIL_UW': (1275, 155), 
            'KIRS_OW': (1225, 215), 'KIRS_UW': (1230, 260), 'FÜRF_OW': (1250, 395), 'FÜRF_UW': (1255, 440), 
            'VILL_OW': (1075, 550), 'VILL_UW': (1070, 580), 'RUNK_OW': (1000,540), 'RUNK_UW': (950,540), 
            'LIMB_OW': (810,570), 'LIMB_UW': (690,570), 'DIEZ_OW': (535,640), 'DIEZ_UW': (550,685), 
            'CRAM_OW': (305,815), 'CRAM_UW': (340,840), 'KALK_OW': (258,950), 'KALK_UW': (225,925)}

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


# def calc_velocities(time_differences, loc_coords, locations_order):
#     # vectors = get_vector(loc_coordinates)
#     # velocities = []
#     vector_list = []
#     previous_id = time_differences[0][0]
#     previous_loc2 = time_differences[0][1]
    
#     for loc_pair in time_differences:
#         ID_HEX, loc1, loc2, time_diff = loc_pair
#         # Determine the vector tuple for the movement
#         veclist = []
#         loc1_idx = locations_order.index(loc1)
#         loc2_idx = locations_order.index(loc2)
#         loc1 = loc_coords[loc1]
        
#         for i in range(loc1_idx, loc2_idx):
#             cur_loc = loc_coords[locations_order[i]]
#             next_loc = loc_coords[locations_order[i+1]]
#             x1, y1 = cur_loc
#             x2, y2 = next_loc
#             dx = x2 - x1
#             dy = y2 - y1
#             vector = (dx, dy)
#             veclist.append(vector)
#             # vectorlist.reverse()
#             vec_dist = 0
#         for j in range(len(veclist)):
#             # Calculate the velocity
#             vec_dist += (math.sqrt(veclist[j][0]**2 + veclist[j][1]**2))
#             # berechne Geschwindigkeit und logarhytmire diese
#             velo_norm = int((math.log(vec_dist / time_diff + 1)) * 100)
#             if ID_HEX != previous_id:
#                 loc2 = loc_coords[previous_loc2]
#             vector_list.append((previous_id,loc1,loc2,veclist[j],velo_norm)) 
#             # else:
#             #     vector_list.append((veclist[j],velo_norm))
#         previous_id = ID_HEX
#         previous_loc2 = loc2
#         # velocities.append(velo_norm)
        

    # return vector_list

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

# Initialize dictionary to store positions of each eel at each time step
positions_dict = {}

# Loop over each ID_HEX in the dataframe
for ID_HEX in df['ID_HEX'].unique():
    
    # Get the rows corresponding to the current ID_HEX
    eel_df = df[df['ID_HEX'] == ID_HEX]
    
    # Get the first position of the eel
    first_loc = eel_df.iloc[0]['loc1']
    
    # Initialize elapsed time
    elapsed_time = 0
    
    # Loop over the vectors for the current eel
    for vec, vec_dist, velo_norm in zip(eel_df['vector'],eel_df['vec_dist'], eel_df['velo_norm']):
        
        # Calculate the time it takes to travel the vector
        travel_time = vec_dist / velo_norm
        
        # Calculate the fraction of the vector to be traveled based on elapsed time
        frac_traveled = min(1, elapsed_time / travel_time)
        
        # Update elapsed time
        elapsed_time += travel_time
        
print(df.head())
        




