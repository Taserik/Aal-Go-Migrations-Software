#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 16:06:37 2023

@author: erik
"""

import pandas as pd
import sqlite3
import math

# Create a connection to the SQLite database
conn = sqlite3.connect('mydatabase.db')

# # create a dictionary to map locations to their coordinates
# location_coordinates = {'LÖHN_OW': (1340, 35), 'LÖHN_UW': (1300, 100), 'WEIL_OW': (1308, 140), 'WEIL_UW': (1275, 155), 
#                         'KIRS_OW': (1225, 215), 'KIRS_UW': (1230, 260), 'FÜRF_OW': (1250, 395), 'FÜRF_UW': (1255, 440), 
#                         'VILL_OW': (1075, 550), 'VILL_UW': (1070, 580), 'RUNK_OW': (1000,540), 'RUNK_UW': (950,540), 
#                         'LIMB_OW': (810,570), 'LIMB_UW': (690,570), 'DIEZ_OW': (535,640), 'DIEZ_UW': (550,685), 
#                         'CRAM_OW': (305,815), 'CRAM_UW': (340,840), 'KALK_OW': (258,950), 'KALK_UW': (225,925)}


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

def rm_lead_0(df,col):
    """Entfernt führende Nullen von einer Spalte im Dataframe"""
    ids = df[col].str.lstrip(r'^(0+)')
    df = df.drop(col, axis=1)
    df.insert(0,col,ids)
    return df

def create_eelcards(conn):
    
    cursor = conn.cursor()
    mother = pd.read_pickle('motherpickel.pkl')
    mother = mother.rename(columns={'Datum': 'Messdatum'})
    mother = rm_lead_0(mother,'ID Code')
    # erste Zeile von mother entfernen
    mother = mother.drop(0)
    # den Index um 3 verschieben, um mit Muttertabelle.xlsx zu synchronisieren
    mother.index +=3
    # Formatiere die Spalten von Mother, um sie lesbarer zu machen
    mother['KF'] = mother['KF'].astype('float64').round(2)
    mother['BF'] = mother['BF'].astype('float64').round(2)
    mother['OF'] = mother['OF'].astype('float64').round(2)
    mother['Messdatum'] = pd.to_datetime(mother['Messdatum'])
    mother['Messdatum'] = mother['Messdatum'].dt.date
    mother['Messdatum'] = mother['Messdatum'].apply(lambda x: x.strftime('%d-%m-%Y') if not pd.isna(x) else '')
    
   
    
    # Get unique values of ID_HEX from database
    cursor.execute('SELECT DISTINCT ID_HEX FROM eeltable')
    
    # Create an empty list to store eel cards
    eelcards = []
    
    # Loop through unique ID_HEX values
    for i in cursor.fetchall():
        i = i[0] # extract the ID_HEX value from the tuple
        # Filter mother dataframe for the current ID_HEX value
        eelcard = mother[mother['ID Code'] == i].copy()
    
        # Get unique locations for the current ID_HEX value from the database
        locations_query = f"SELECT DISTINCT Ort FROM eeltable WHERE ID_HEX='{i}'"
        locations = pd.read_sql(locations_query, conn)['Ort'].tolist()
    
        # Get the latest location for the current ID_HEX value from the database
        latest_location_query = f"SELECT Ort FROM eeltable WHERE ID_HEX='{i}' ORDER BY DATUM DESC LIMIT 1"
        latest_location_result = pd.read_sql(latest_location_query, conn)
    
        if not latest_location_result.empty:
            latest_location = latest_location_result['Ort'].iloc[0]
            latest_locations_list = [latest_location]
        else:
            latest_locations_list = []
            latest_location = None
    
        # Create string of locations for each eel
        location_strings = [','.join(locations)]
    
        # Add 'Locations' and 'latest_loc' column to eelcard
        eelcard.loc[:, 'Location'] = location_strings
        eelcard.loc[:, 'latest_loc'] = latest_locations_list
    
        # Append eelcard to list of eel cards
        eelcards.append(eelcard)
    
    # Concatenate all eel cards into a single dataframe
    eelcard_df = pd.concat(eelcards, ignore_index=True)
    # Strip the entire dataframe from whitespaces
    eelcard_df = eelcard_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    cursor.close()
    return eelcard_df


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


# def get_vector(loc1, loc2, loc_coordinates):
#     """
#     Returns a tuple of vectors between the two locations.
#     """
#     x1, y1 = loc_coordinates[loc1]
#     x2, y2 = loc_coordinates[loc2]
#     dx = x2 - x1
#     dy = y2 - y1
#     return (dx, dy)




# def calc_vectors(conn,locations_in_order):
#     """Calculates the vectors between 2 adjacent locations according between 
#     all the different locations in order"""
#     cursor = conn.cursor()
#     vectors = {}
#     for i in range(len(locations_in_order)-1):
#             try:
#                 # Look up the coordinates in the database
#                 cursor.execute("SELECT x_coordinate, y_coordinate FROM eeltable WHERE Ort=?", (locations_in_order[i],))
#                 x1, y1 = cursor.fetchone()
#                 cursor.execute("SELECT x_coordinate, y_coordinate FROM eeltable WHERE Ort=?", (locations_in_order[i+1],))
#                 x2, y2 = cursor.fetchone()
                
#                 # Calculate the vector and store it in the dictionary
#                 vector = (x2 - x1, y2 - y1)
#                 vectors[(locations_in_order[i], locations_in_order[i+1])] = vector
#             except TypeError:
#                 print(f"{locations_in_order[i]} or {locations_in_order[i+1]} not found in database")
#     cursor.close()
#     return vectors


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


eelcards_df = create_eelcards(conn)
vector_dict = get_vector(loc_coordinates)
time_diffs,time_diffs_check,stationary_time = time_differences(conn,locations_order)

# def calc_velocities(locations_order,time_differences):
#     distances = calc_distances(loc_coordinates)
#     velocities = []

#     for loc_pair in time_differences.keys():
        
#         dist = [d[2] for d in distances if d[:2] == loc_pair[1:]][0]
#         velo = dist / time_differences[loc_pair]
     
#         velocities.append(velo)
#     return velocities
def calc_velocities(time_differences, loc_coordinates):
    distances = calc_distances(loc_coordinates)
    # vectors = get_vector(loc_coordinates)
    velocities = []

    for loc_pair in time_differences:
        ID_HEX, loc1, loc2, time_diff = loc_pair
        
        # Calculate the velocity
        dist = [d[2] for d in distances if d[:2] == (loc1, loc2)][0]
        velo = dist / time_diff
        
        # Get the vector
        # vector = vectors[(loc1, loc2)]
        velocities.append((ID_HEX, loc1, loc2, velo))

    return velocities

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

import time

def move_eels(canvas, velocities, movement_vectors):
    for velo in velocities:
        # Get the movement vectors for this eel
        loc1, loc2 = velo[1], velo[2]
        vectors = movement_vectors[(loc1, loc2)]
        
        # Get the current position of the eel
        eel_id = velo[0]
        eel_x, eel_y = canvas.coords(eel_id)
        
        # Move the eel along each vector at the calculated velocity
        for vector in vectors:
            # Calculate the distance to travel
            distance = (vector[2]**2 + vector[3]**2)**0.5
            
            # Calculate the time it should take to travel the distance
            time_to_travel = distance / velo[4]
            
            # Calculate the amount to move the eel in each direction per millisecond
            x_speed = vector[2] / time_to_travel / 1000
            y_speed = vector[3] / time_to_travel / 1000
            
            # Move the eel along the vector
            start_time = time.time()
            while time.time() - start_time < time_to_travel:
                eel_x += x_speed
                eel_y += y_speed
                canvas.coords(eel_id, eel_x, eel_y)
                canvas.update()
            time.sleep(0.01)




# Close the database connection and the cursor
conn.close()








