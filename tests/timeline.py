# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:24:40 2023

@author: TheRickestRick
"""

import tkinter as tk
from PIL import Image,ImageTk
from fetch_data import df
import datetime as dt

def timeline(canvas):
    
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
    total_timespan = (max_date - min_date).days
    
    # Create canvas and timeline line
    timeline_line = canvas.create_line(50, canvas_height - 70, canvas_width-50, canvas_height -70, fill='black', width=3)
    
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
    
    # Set the speed of the animation (in pixels per millisecond)
    animation_speed = 2.00
    
    # Create the red line
    red_line = canvas.create_line(50, canvas_height - 60, 50, canvas_height - 80, fill='red', width=3)
    
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
    
    
    # eelmap.mainloop()
