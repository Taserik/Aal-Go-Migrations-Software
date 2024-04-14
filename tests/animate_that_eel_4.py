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
import datetime as dt
# from timeline_2 import timeline

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
# timeline(canvas, sorted_eel_list[4])

def timeline(canvas,df):
    global canvas_height
    global canvas_width
    
    # Define start and end date of the timeline
    min_date_xl = df['DATUM'].min()
    max_date_xl = df['DATUM'].max()
    
    def xldate_to_datetime(xldate):
        '''Converts a date from Excel serial number to datetime object'''
        temp = dt.datetime(1899, 12, 30)
        delta = dt.timedelta(days=xldate)
        return temp+delta
    
    min_date = xldate_to_datetime(min_date_xl)
    max_date = xldate_to_datetime(max_date_xl)
    
    # Get actual canvas width
    canvas_width = canvas.winfo_reqwidth()
    canvas_height = canvas.winfo_reqheight()
    
    # Calculate total time span in days
    total_timespan = (max_date - min_date).total_seconds()
    
    # Create canvas and timeline line
    timeline_line = canvas.create_line(50, canvas_height - 70, canvas_width-50, canvas_height -70, fill='black', width=3)
    
    start_date = min_date.month
    end_date = max_date.month
    if  start_date == 12 and end_date == 12:
        start_date = 12
    elif start_date == 12:
        start_date = 1
    
    
    for month in range(start_date,end_date+1):
        
        if start_date == 12:
            curr_month_start = dt.datetime(max_date.year,month,31)
            days_since_start = (curr_month_start-min_date).total_seconds()
        else:
            curr_month_start = dt.datetime(max_date.year,month, 1)
            # Calculate the number of days between the start of the timeline and the start of the current month
            days_since_start = (curr_month_start - min_date).total_seconds()
        
        marker_x = 50 + (canvas_width-100) * (days_since_start / total_timespan)
    
        # Draw the vertical line at the marker position
        canvas.create_line(marker_x, canvas_height - 85, marker_x, canvas_height - 55, fill='black', width=2)
        
        # Add a label for the current month below the marker
        canvas.create_text(marker_x, canvas_height - 45, text=curr_month_start.strftime('%B %Y'), fill='black', font=('Helvetica', '10'))
    
    # Add markers for the start and end date
    start_marker_x = 50
    canvas.create_line(start_marker_x, canvas_height - 85, start_marker_x, canvas_height - 55 , fill='black', width=2)
    canvas.create_text(start_marker_x, canvas_height - 45, text=min_date.strftime('%d-%m-%Y'), fill='black', font=('Helvetica', '10'))
    
    end_marker_x = canvas_width - 50
    canvas.create_line(end_marker_x, canvas_height - 85, end_marker_x, canvas_height - 55, fill='black', width=2)
    canvas.create_text(end_marker_x, canvas_height - 45, text=max_date.strftime('%d-%m-%Y'), fill='black', font=('Helvetica', '10'))

timeline(canvas, sorted_eel_list[4])

snare = 1

def make_dot(canvas, row, df):
    global oval_id
    loc1 = row['loc1']
    anim_locs = row['path']
    if anim_locs is not None:
        oval_id = canvas.create_oval(anim_locs[0][0],anim_locs[0][1],anim_locs[0][0]+5,anim_locs[0][1]+5, fill = 'red')
    
    # Set the speed of the animation (in pixels per animation cycle)
    animation_speed = 2
    
    # the sum of the duration an eel takes for it's whole path
    dur_sum = df['duration'].sum()
    
    # calculate the time_delay for the animation
    animation_time = int(dur_sum/(0.1280/animation_speed))
    
    
    
    # Define a function to move the line
    def move_line():
       
        # Create the red line
        red_line = canvas.create_line(50, canvas_height - 60, 50, canvas_height - 80, fill='red', width=3)
        
        # Get the current position of the line
        x1, y1, x2, y2 = canvas.coords(red_line)
        
        # Move the line to the right by the animation speed
        red_move = canvas.move(red_line, animation_speed, 0)
        
        # If the line has reached the end of the timeline, reset its position to the left
        if x2 >= canvas_width - 50:
            canvas.after_cancel(red_move)
        
        # Call this function again after a short delay
        canvas.after(animation_time, move_line)
    
        # Start the animation
        if red_line is not None:
            move_line()
    
        red_line = None
    
    def anim_dot():
        global oval_id
        if anim_locs is not None:
            for loc in anim_locs:
              
                x, y = loc
                
                # if oval_id is not None:
                    # canvas.delete(oval_id)
                canvas.coords(oval_id,x, y, x, y)
                
                # canvas.update()
                
                # canvas.after(int(snare*1000*row['duration']/len(row['path'])))
                canvas.after(10,anim_dot)
           
                
        else:
            x, y = loc
            oval_id = canvas.create_oval(x, y, x+5, y+5, fill='red')
            canvas.update()
    anim_dot()
    # if oval_id is not None:
    #     canvas.delete(oval_id)

# assuming df is your pandas dataframe
# for eel_df in eel_list:

# for index, row in sorted_eel_list[3].iterrows():
#     if row['loc2'] != 'stationary':
#         make_dot(canvas, row, sorted_eel_list[4])
#     else:
#         canvas.after(int(10*row['duration']*snare))


for index, row in sorted_eel_list[4].iterrows():
    make_dot(canvas,row,sorted_eel_list[4])


eelmap.mainloop()

  
# path_sum = 0

# for path in df['path']:
#     if path is not None:
#         path_sum += len(path)

