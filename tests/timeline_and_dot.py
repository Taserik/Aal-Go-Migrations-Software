# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:24:40 2023

@author: TheRickestRick
"""

import datetime as dt
import pandas as pd
import tkinter as tk
import json

class Timeline:
    def __init__(self, canvas, df, animation_speed=2.0):
        self.canvas = canvas
        self.df = df
        self.animation_speed = animation_speed
        
        # Define start and end date of the timeline
        min_date_xl = self.df['DATUM'].min()
        max_date_xl = self.df['DATUM'].max()
        
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
        total_timespan = (max_date - min_date).days
        
        # Create canvas and timeline line
        timeline_line = self.canvas.create_line(50, canvas_height - 70, canvas_width-50, canvas_height -70, fill='black', width=3)
        
        start_date = min_date.month
        if start_date == 12:
            start_date = 1
        end_date = max_date.month
        
        for month in range(start_date,end_date+1):
            curr_month_start = dt.datetime(max_date.year,month, 1)
            # Calculate the number of days between the start of the timeline and the start of the current month
            days_since_start = (curr_month_start - min_date).days
            
            marker_x = 50 + (canvas_width-100) * (days_since_start / total_timespan)
        
            # Draw the vertical line at the marker position
            self.canvas.create_line(marker_x, canvas_height - 85, marker_x, canvas_height - 55, fill='black', width=2)
            
            # Add a label for the current month below the marker
            self.canvas.create_text(marker_x, canvas_height - 45, text=curr_month_start.strftime('%B %Y'), fill='black', font=('Helvetica', '10'))
        
        # Add markers for the start and end date
        start_marker_x = 50
        self.canvas.create_line(start_marker_x, canvas_height - 85, start_marker_x, canvas_height - 55 , fill='black', width=2)
        self.canvas.create_text(start_marker_x, canvas_height - 45, text=min_date.strftime('%d-%m-%Y'), fill='black', font=('Helvetica', '10'))
        
        end_marker_x = canvas_width - 50
        self.canvas.create_line(end_marker_x, canvas_height - 85, end_marker_x, canvas_height - 55, fill='black', width=2)
        self.canvas.create_text(end_marker_x, canvas_height - 45, text=max_date.strftime('%d-%m-%Y'), fill='black', font=('Helvetica', '10'))
        
        # Create the red line
        self.red_line = self.canvas.create_line(50, canvas_height - 60, 50, canvas_height - 80, fill='red', width=3)
            

class Dot:
    def __init__(self, canvas, start_pos, color):
        self.canvas = canvas
        self.color = color
        self.id = self.canvas.create_oval(start_pos[0][0]-5, start_pos[0][1]-5, start_pos[0][0]+5, start_pos[0][1]+5, fill=self.color)
        self.path_start = 0
        self.path_end = len(start_pos)
        self.path = start_pos
        self.speed = 2

    def update(self):
        if self.path_start < self.path_end - 1:
            self.path_start += 1
            self.path = self.path[self.path_start:self.path_end]

        x, y, _, _ = self.canvas.coords(self.id)
        x += (self.path[0][0] - x) * self.speed / 100
        y += (self.path[0][1] - y) * self.speed / 100
        self.canvas.coords(self.id, x-5, y-5, x+5, y+5)



# define the list of tuples of the coordinates you want the animation to be in
with open("anim_vecs.json", "r", encoding="utf-8") as f:
    coordinates = json.load(f)

with open("locations.json", "r", encoding="utf-8") as f:
    loc_coords = json.load(f)

loc_coords = {k: tuple(int(x) for x in v) for k, v in loc_coords.items()}
loc_list = []
for loc in loc_coords:
    loc_list.append(loc_coords[loc])
coordinates = [tuple(map(int, sublist)) for sublist in coordinates]    

eelmap = tk.Tk()
eelmap.geometry("1280x840")  # Set size of root window to 1920x1080 pixels
canvas = tk.Canvas(eelmap,width = 1280,height = 840 )
canvas.pack(fill=tk.BOTH, expand=True)

dots = []

for loc in loc_coords:
    dot = Dot(canvas, loc_list, 'green') # create a Dot for each location
    dots.append(dot) # add the new Dot instance to the dots list

    
def update_dots():
    for dot in dots:
        dot.update()
    canvas.after(10, update_dots)

update_dots()

eelmap.mainloop()









