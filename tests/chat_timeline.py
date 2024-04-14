# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:58:43 2023

@author: TheRickestRick
"""


import tkinter as tk
from PIL import Image, ImageTk
from fetch_data import df
import datetime as dt

root = tk.Tk()
canvas = tk.Canvas(root, width=1280, height=840)
canvas.pack()

id_hex_list = df['ID_HEX'].unique()

eel_list = []
for i in id_hex_list:
    eel_df = df.loc[df['ID_HEX'] == i, ['ID_HEX', 'loc1', 'loc2', 'duration', 'DATUM', 'path']]
    eel_list.append(eel_df)

sorted_eel_list = sorted(eel_list, key=lambda x: x['DATUM'].min())

# Initialize current index
curr_index = 0
line_x = 50

def timeline(canvas, df):
    # Define start and end date of the timeline
    min_date_xl = df['DATUM'].min()
    max_date_xl = df['DATUM'].max()

    def xldate_to_datetime(xldate):
        '''Converts a date from Excel serial number to datetime object'''
        temp = dt.datetime(1899, 12, 30)
        delta = dt.timedelta(days=xldate)
        return temp + delta

    min_date = xldate_to_datetime(min_date_xl)
    max_date = xldate_to_datetime(max_date_xl)

    # Get actual canvas width and height
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Calculate total time span in seconds
    total_timespan = (max_date - min_date).total_seconds()

    # Create canvas and timeline line
    timeline_line = canvas.create_line(50, canvas_height - 70, canvas_width - 50, canvas_height - 70, fill='black',
                                       width=3)

    # Calculate the number of months between the start and end date
    num_months = (max_date.year - min_date.year) * 12 + max_date.month - min_date.month

    for i in range(num_months + 1):
        curr_month = min_date + dt.timedelta(days=30 * i)

        # Calculate the number of seconds between the start of the timeline and the start of the current month
        seconds_since_start = (curr_month - min_date).total_seconds()

        # Calculate the marker x-coordinate based on the number of seconds
        marker_x = 50 + ((canvas_width - 100) * (seconds_since_start / total_timespan))

        # Draw the vertical line at the marker position
        canvas.create_line(marker_x, canvas_height - 85, marker_x, canvas_height - 55, fill='black', width=2)

        # Add a label for the current month below the marker
        canvas.create_text(marker_x, canvas_height - 45, text=curr_month.strftime('%B %Y'), fill='black',
                           font=('Helvetica', '10'))

    # Add markers for the start and end date
    canvas.create_line(50, canvas_height - 85, 50, canvas_height - 55, fill='black', width=2)
    canvas.create_text(50, canvas_height - 45, text=min_date.strftime('%d-%m-%Y'), fill='black',
                       font=('Helvetica', '10'))

    canvas.create_line(canvas_width - 50, canvas_height - 85, canvas_width - 50, canvas_height - 55, fill='black',
                       width=2)
    canvas.create_text(canvas_width - 50, canvas_height - 45, text=max_date.strftime('%d-%m-%Y'), fill='black',
                       font=('Helvetica', '10'))

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
    oval_id = canvas.create_oval(x, y, x + 5, y + 5, fill='red')

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
            canvas.coords(oval_id, x, y, x + 5, y + 5)
    
            if df['path'].iloc[curr_index] is not None:
                path_len = len(df['path'].iloc[curr_index])
                path_frac = path_len / path_sum
                px_frac = path_frac * (canvas_width - 100)  # Adjust the value based on your canvas width
                line_x = 50 + ((dur / dur_sum) * px_frac / path_sum)
    
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
