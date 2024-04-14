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
timeline(canvas, sorted_eel_list[3])

snare = 10

import time

def animate_dot(canvas, row):
    loc1 = row['loc1']
    anim_locs = row['path']
    oval_id = None
    for loc in anim_locs:
        x, y = loc
        if oval_id is not None:
            canvas.delete(oval_id)
        oval_id = canvas.create_oval(x, y, x+5, y+5, fill='red')
        canvas.update()
        time.sleep(row['duration']/len(row['path'])*snare)
    else:
        x, y = loc1
        oval_id = canvas.create_oval(x, y, x+5, y+5, fill='red')
        canvas.update()
    
    # if oval_id is not None:
    #     canvas.delete(oval_id)

# assuming df is your pandas dataframe
# for eel_df in eel_list:

for index, row in sorted_eel_list[3].iterrows():
    if row['loc2'] != 'stationary':
        animate_dot(canvas, row)
        time.sleep(0.1) # adjust the pause time to your liking
    else:
        time.sleep(row['duration']*snare)


eelmap.mainloop()


