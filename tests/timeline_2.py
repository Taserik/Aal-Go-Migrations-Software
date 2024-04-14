# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:24:40 2023

@author: TheRickestRick
"""

import tkinter as tk
from PIL import Image,ImageTk
from fetch_data import df
import datetime as dt

root = tk.Tk()
canvas = tk.Canvas(root, width=1280, height=840)
canvas.pack()

id_hex_list = df['ID_HEX'].unique()

eel_list = []
for i in id_hex_list:
    eel_df = df.loc[df['ID_HEX'] == i , ['ID_HEX','loc1', 'loc2', 'duration', 'DATUM','path']]
    eel_list.append(eel_df)

sorted_eel_list = sorted(eel_list, key=lambda x: x['DATUM'].min())

# Initialize current index
curr_index = 0

line_x = 50

def timeline(canvas,df):
    
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
    
    # Set the speed of the animation (in pixels per animation cycle)
    # animation_speed = 2
    
    # the sum of the duration an eel takes for its whole path
    dur_sum = df['duration'].sum()
    
    # Calculate the total path length
    path_sum = sum(len(path) for path in df['path'] if path is not None)
    
    # Get the initial position for the oval
    for first in df['path']:
        if first is not None:
            x, y = first[0]
            break
    
    # Create the oval
    oval_id = canvas.create_oval(x, y, x+5, y+5, fill='red')
    
    # Create the red line
    red_line = canvas.create_line(50, canvas_height - 60, 50, canvas_height - 80, fill='red', width=3)
    
    def animate():
        global curr_index
        global line_x
    
        if curr_index >= len(df['path']):
            return
    
        # Get the current path and duration
        path = df['path'].iloc[curr_index]
        dur = df['duration'].iloc[curr_index]
    
        # Skip None values in path or duration
        if path is None or dur is None:
            curr_index += 1
            canvas.after(10, animate)
            return
    
        # Draw the oval at the current location
        for x, y in path:
            # Move the oval
            canvas.coords(oval_id, x, y, x+5, y+5)
    
            if df['path'].iloc[curr_index] is not None:
                path_len = len(df['path'].iloc[curr_index])
                path_frac = path_len / path_sum
                px_frac = path_frac * 1284  # Adjust the value as needed based on your canvas width
                line_x += (dur / dur_sum) * px_frac / path_sum
    
            canvas.coords(red_line, line_x, canvas_height - 60, line_x, canvas_height - 80)
    
            canvas.update()
            # Delay between each position update (adjust the value as needed)
            canvas.after(10)
    
        # Calculate the next index
        curr_index += 1
    
        # Call this function again after the specified duration
        animate()
        
    # Start the animation
    animate()

timeline(canvas, sorted_eel_list[3])

root.mainloop()









   # # Define a function to move the line
   # def animate(index=0):
   #     # Get the current position of the line
   #     x1, y1, x2, y2 = canvas.coords(red_line)
   #     anim_locs = df['path']
   #     oval_id = None
   #     for loc in anim_locs:
   #         if loc is not None:
   #             x, y = loc
   #             if oval_id is not None:
   #                 canvas.delete(oval_id)
   #             oval_id = canvas.create_oval(x, y, x+5, y+5, fill='red')
   #             canvas.update()
   #             else:
   #                 x, y = loc
   #                 oval_id = canvas.create_oval(x, y, x+5, y+5, fill='red')
   #                 canvas.update()
       
   #     # Move the line to the right by the animation speed
   #     canvas.coords(red_line, x1+1, y1, x2+1, y2)
       
   #     # If the line has reached the end of the timeline, reset its position to the left
   #     if x2 >= canvas_width - 50:
   #         return
       
   #     # Call this function again after a short delay
   #     canvas.after(animation_time, animate, index + 1)