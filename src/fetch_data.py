# -*- coding: utf-8 -*-
"""
Created on Wed May 10 03:22:44 2023

@author: TheRickestRick
"""
import pandas as pd
import sqlite3
from support_vectors import path_dict

conn = sqlite3.connect('mydatabase.db')

def fetch_data(conn):
    
    cursor = conn.cursor()
    rangequery = "SELECT ID_HEX, Ort, Serial_XLDate, DATUM FROM eeltable ORDER BY ID_HEX,Serial_XLDate ASC"
    # execute the query and store the results in a list
    rows = cursor.execute(rangequery).fetchall()   
        
    # get a list of all distinct ID_HEX values
    id_hex_values = set(row[0] for row in rows)
    
    # create lists to store the time differences for each eel at each location
    # and the stationary time spent
    id_hexs = []
    loc1_list = []
    loc2_list = []
    diffs_list = []
    dates_list = []
    
    # get the ID_HEX and location for the current row
    
    # loop through the distinct ID_HEX values
    for id_hex in id_hex_values:
    
        # select only the rows that match the current ID_HEX value
        rows_for_id = [row for row in rows if row[0] == id_hex]
        start_station_date = rows_for_id[0][2]
        
        for i in range(len(rows_for_id)-1):
            
            # get the current row and the next row in the list
            row1 = rows_for_id[i]
            row2 = rows_for_id[i+1]
            
            location1 = row1[1]
            
            if row1[1] != row2[1]:
                
                end_station_date = row1[2]
                
                stationary_time = end_station_date - start_station_date
                                
                location2 = "stationary"
                id_hexs.append(id_hex)
                loc1_list.append(location1)
                loc2_list.append(location2)
                diffs_list.append(stationary_time)
                dates_list.append(start_station_date)
                                
                start_station_date = row2[2]
                
                diff = row2[2] - row1[2]
                
                location2 = row2[1]

                if diff > 0 and diff < 365:
                    # add the values to the lists
                    id_hexs.append(id_hex)
                    loc1_list.append(location1)
                    loc2_list.append(location2)
                    diffs_list.append(diff)
                    dates_list.append(end_station_date)
                    
                else:
                    print("Die Wanderzeit ist zu klein oder zu groß, um Sinn zu ergeben")
    
    df = pd.DataFrame({
        'ID_HEX': id_hexs,
        'loc1': loc1_list,
        'loc2': loc2_list,
        'duration': diffs_list,
        'DATUM': dates_list
    })
    
    df['path'] = None
    
    for i, row in df.iterrows():
        key = str(row[1]) + ',' + str(row[2])
        if row[2] == 'stationary':
            df.at[i, 'path'] = None
        elif key in path_dict:
            df.at[i,'path'] = path_dict[key]
        else:
            key_reversed = str(row[2]) + ',' + str(row[1])
            if key_reversed in path_dict:
                df.at[i, 'path'] = list(reversed(path_dict[key_reversed]))
            else:
                continue
    return df  

df = fetch_data(conn)   






