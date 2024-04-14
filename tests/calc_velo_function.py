# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:11:53 2023

@author: TheRickestRick
"""

def calc_velocities(time_diffs, loc_coords, locations_order):    

    # Create empty lists to store information
    ID_HEX_list = []
    loc1_list = []
    loc2_list = []
    velo_norm_list = []
    time_diff_list  = []
    action_dates = []

    
    for loc_pair in time_diffs:
        ID_HEX, loc1, loc2, time_diff, date = loc_pair
        
        if loc2 == "stationary":
            ID_HEX_list.append(ID_HEX)
            loc1_list.append(loc_coords[loc1])
            loc2_list.append("stationary")
            velo_norm_list.append(0)
            time_diff_list.append(time_diff)
            action_dates.append(date)
        else:
            # Determine the vector tuple for the movement
            veclist = []
            loc1_idx = locations_order.index(loc1)
            loc2_idx = locations_order.index(loc2)
            loc1 = loc_coords[loc1]
            loc2 = loc_coords[loc2]
            
            for i in range(loc1_idx, loc2_idx):
                # find out the needed vectors between loc1_idx and loc2_idx and
                # append them to a list. Use np for vector calculation.
                cur_loc = np.array(loc_coords[locations_order[i]])
                next_loc = np.array(loc_coords[locations_order[i+1]])
                vector = next_loc - cur_loc
                veclist.append(vector)
                vec_dist = 0
                
            # Calculate the velocity for all vectors in the list
            vec_dist = sum(math.sqrt(vec[0]**2 + vec[1]**2) for vec in veclist)
            velo_norm = int((math.log(vec_dist / time_diff + 1)) * 100)

            # Append information to lists
            ID_HEX_list.append(ID_HEX)
            loc1_list.append(loc1)
            loc2_list.append(loc2)
            time_diff_list.append(time_diff)
            velo_norm_list.append(velo_norm)
            action_dates.append(date)
            
    # Create dataframe from lists
    df = pd.DataFrame({
        'ID_HEX': ID_HEX_list,
        'loc1': loc1_list,
        'loc2': loc2_list,
        'duration': time_diff_list,
        'velo_norm': velo_norm_list,
        'DATUM': action_dates
    })
    
    return df