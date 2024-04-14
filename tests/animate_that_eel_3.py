# -*- coding: utf-8 -*-
"""
Created on Wed May 10 01:30:50 2023

@author: TheRickestRick
"""
import math
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk
from fetch_data import df
import json
from timeline_2 import timeline

# define the list of tuples of the coordinates you want the animation to be in
with open("anim_vecs.json", "r", encoding="utf-8") as f:
    anim_locs = json.load(f)    

# open the all locations the 
with open("locations.json", "r", encoding="utf-8") as f:
    loc_coords = json.load(f)
loc_coords = {k: tuple(int(x) for x in v) for k, v in loc_coords.items()}


id_hex_list = df['ID_HEX'].unique()

eel_list = []
for i in id_hex_list:
    eel_df = df.loc[df['ID_HEX'] == i , ['ID_HEX','loc1', 'loc2', 'duration', 'DATUM','path']]
    eel_list.append(eel_df)

sorted_eel_list = sorted(eel_list, key=lambda x: x['DATUM'].min())
# eel_df['anim_locs'] = [None,anim_locs[4:53],None,anim_locs[52:115],None,anim_locs[114:167],None,anim_locs[166:326],None,anim_locs[325:348],None,anim_locs[347:536],None,anim_locs[535:657]]




eelmap = tk.Tk()
map_img_path = 'lahn2.png'
map_image = Image.open(map_img_path)
map_photo = ImageTk.PhotoImage(map_image)

eelmap.geometry("1280x840")  # Set size of root window to 1920x1080 pixels
canvas = tk.Canvas(eelmap, width=map_image.width, height=map_image.height)
canvas.create_image(0, 0, image=map_photo, anchor=tk.NW)
canvas.pack(fill=tk.BOTH, expand=True)
import time

snare = 1000

def animate_redline(canvas, pathcount, red_line):
    # Get actual canvas width
    canvas_width = canvas.winfo_reqwidth()
    canvas_height = canvas.winfo_reqheight()

    # If no red line is provided, create a new one
    if red_line is None:
        red_line = canvas.create_line(50, canvas_height - 60, 50, canvas_height - 80, fill='red', width=3)

    # Set the speed of the animation (in pixels per millisecond)
    # the timeline is 1182 pixels long, because we have a padding of 50 on each side
    animation_speed = 1182 / pathcount # assuming 1000 milliseconds in a second

    # Define a function to move the line
    def move_line():
        # Get the current position of the line
        x1, y1, x2, y2 = canvas.coords(red_line)

        # Move the line to the right by the animation speed
        canvas.move(red_line, animation_speed, 0)

        # If the line has reached the end of the timeline, reset its position to the left
        if x2 >= canvas_width - 50:
            canvas.coords(red_line, 50, canvas_height - 60, 50, canvas_height - 80)

        # Call this function again after a short delay
        canvas.after(10, move_line)

    # Start the animation
    move_line()

    # Return the red line so it can be used again if needed
    return red_line



def animate_dot(canvas, row, red_line):
    loc1 = loc_coords[row['loc1']]
    anim_locs = row['path']
    oval_id = None
    if anim_locs is not None:
        for loc in anim_locs:
            x, y = loc
            if oval_id is not None:
                canvas.delete(oval_id)
            oval_id = canvas.create_oval(x, y, x+5, y+5, fill='red')
            canvas.update()
            # time.sleep(row['duration']/len(row['path'])*snare)
            canvas.after(int(row['duration']/len(anim_locs)*snare), animate_dot, canvas, row, red_line)


    else:
        x, y = loc1
        oval_id = canvas.create_oval(x, y, x+5, y+5, fill='red')
        canvas.update()
        red_line = animate_redline(canvas, pathcount, red_line) # pass red_line to animate_redline
    
    if oval_id is not None:
        canvas.delete(oval_id)
        
    canvas.after(int(row['duration']*snare), animate_dot, canvas, row, red_line)

    return red_line

# count the number of pathes the animation has to go along at to calculate 
# the speed for the timeline animation
pathcount = 0

for idx, rows in sorted_eel_list[3].iterrows():
    if rows['path'] is not None:
        pathcount += len(rows['path'])

timeline_created = False
red_line = None




for index, row in sorted_eel_list[3].iterrows():
    red_line = animate_dot(canvas, row, red_line)
    if not timeline_created:
        timeline(canvas, sorted_eel_list[3])
        timeline_created = True
    if row['loc2'] != 'stationary':
        time.sleep(0.1) # adjust the pause time to your liking
    else:
        time.sleep(row['duration']*snare)
        
eelmap.mainloop()


# # assuming df is your pandas dataframe
# for eel_df in sorted_eel_list:

#     for index, row in eel_df.iterrows():
#         if row['loc2'] != 'stationary':
#             animate_dot(canvas, row)
#             time.sleep(0.1) # adjust the pause time to your liking
#         else:
#             time.sleep(row['duration']*snare)

# # assuming df is your pandas dataframe
# for i, eel_df in enumerate(sorted_eel_list):
#     if i >= 2:  # skip the first two elements in the list