# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:24:40 2023

@author: TheRickestRick
"""

import tkinter as tk
from PIL import Image,ImageTk
from animate_eels_3 import df
import datetime as dt

import datetime as dt

class Timeline:
    def __init__(self, canvas, df):
        self.canvas = canvas
        self.df = df
        self.min_date_xl = self.df['DATUM'].min()
        self.max_date_xl = self.df['DATUM'].max()
        self.canvas_width = self.canvas.winfo_reqwidth()
        self.canvas_height = self.canvas.winfo_reqheight()
        self.min_date = self.xldate_to_datetime(self.min_date_xl)
        self.max_date = self.xldate_to_datetime(self.max_date_xl)
        self.total_timespan = (self.max_date - self.min_date).days
        self.timeline_line = self.canvas.create_line(50, self.canvas_height - 70, self.canvas_width - 50, self.canvas_height - 70, fill='black', width=3)
        self.start_date = self.min_date.month if self.min_date.month != 12 else 1
        self.end_date = self.max_date.month
        self.animation_speed = 2.0
        self.red_line = self.canvas.create_line(50, self.canvas_height - 60, 50, self.canvas_height - 80, fill='red', width=3)
        self.move_line()

    def xldate_to_datetime(self, xldate):
        '''Converts a date from Excel serial number to datetime object'''
        temp = dt.datetime(1899, 12, 30)
        delta = dt.timedelta(days=xldate)
        return temp + delta
    
    def move_line(self):
        # Get the current position of the line
        x1, y1, x2, y2 = self.canvas.coords(self.red_line)
        
        # Move the line to the right by the animation speed
        self.canvas.move(self.red_line, self.animation_speed, 0)
        
        # If the line has reached the end of the timeline, reset its position to the left
        if x2 >= self.canvas_width - 50:
            self.canvas.coords(self.red_line, 50, self.canvas_height - 60, 50, self.canvas_height - 80)
        
        # Call this function again after a short delay
        self.canvas.after(10, self.move_line)
    
    def create_timeline(self):
        for month in range(self.start_date, self.end_date + 1):
            curr_month_start = dt.datetime(self.max_date.year, month, 1)
            days_since_start = (curr_month_start - self.min_date).days
            marker_x = 50 + (self.canvas_width - 100) * (days_since_start / self.total_timespan)
            self.canvas.create_line(marker_x, self.canvas_height - 85, marker_x, self.canvas_height - 55, fill='black', width=2)
            self.canvas.create_text(marker_x, self.canvas_height - 45, text=curr_month_start.strftime('%B %Y'), fill='black', font=('Helvetica', '10'))
        
        # Add markers for the start and end date
        start_marker_x = 50
        self.canvas.create_line(start_marker_x, self.canvas_height - 85, start_marker_x, self.canvas_height - 55 , fill='black', width=2)
        self.canvas.create_text(start_marker_x, self.canvas_height - 45, text=self.min_date.strftime('%d-%m-%Y'), fill='black', font=('Helvetica', '10'))
        
        end_marker_x = self.canvas_width - 50
        self.canvas.create_line(end_marker_x, self.canvas_height - 85, end_marker_x, self.canvas_height - 55 , fill='black', width=2)
        self.canvas.create_text(end_marker_x, self.canvas_height - 45, text=self.max_date.strftime('%d-%m-%Y'), fill='black', font=('Helvetica', '10'))
        
        # Add labels for each milestone
        for i, milestone in enumerate(self.milestones):
            milestone_date = milestone['date']
            days_since_start = (milestone_date - self.min_date).days
            marker_x = 50 + (self.canvas_width - 100) * (days_since_start / self.total_timespan)
            self.canvas.create_line(marker_x, self.canvas_height - 70, marker_x, self.canvas_height - 55 , fill='black', width=2)
            self.canvas.create_text(marker_x, self.canvas_height - 40, text=milestone['label'], fill='black', font=('Helvetica', '10'))
            self.canvas.create_text(marker_x, self.canvas_height - 25, text=milestone_date.strftime('%d-%m-%Y'), fill='black', font=('Helvetica', '8'))

