#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:05:46 2023

@author: erik
"""

import tkinter as tk
from PIL import Image, ImageTk
import json



with open("vectors.json", "r", encoding="utf-8") as f:
    loc_coords = json.load(f)
# print(loc_coords)
class Location:
    def __init__(self, canvas, loc_coords):
        self.canvas = canvas
        self.loc_coords = loc_coords
        self.dots = {}
        self.active = None
        # self.offset = (0, 0)
        self.fill = None  # define fill as an instance variable
        self.draw_dots()

    def draw_dots(self):
        for key, val in self.loc_coords.items():
            dot = self.canvas.create_oval(val[0] - 3, val[1] - 3, val[0] + 3, val[1] + 3, fill="red", tags=key)
            label = self.canvas.create_text(val[0], val[1] - 20, text=key, font=("Arial", 1), fill="black")
            self.dots[key] = {'dot': dot, 'label': label}
            self.canvas.tag_bind(dot, '<ButtonPress-1>', self.on_dot_click)
            self.canvas.tag_bind(dot, '<B1-Motion>', self.on_dot_move)
            self.canvas.tag_bind(dot, '<ButtonRelease-1>', self.on_dot_release)

    def on_dot_click(self, event):
        self.active = event.widget.find_closest(event.x, event.y)[0]
        # self.offset = (event.x - self.canvas.coords(self.active)[0], event.y - self.canvas.coords(self.active)[1])

    def on_dot_move(self, event):
        if self.active:
            new_x = event.x
            new_y = event.y
            if new_x > self.canvas.winfo_width():
                new_x = self.canvas.winfo_width()
            elif new_x < 0:
                new_x = 0
            if new_y > self.canvas.winfo_height():
                new_y = self.canvas.winfo_height()
            elif new_y < 0:
                new_y = 0
            # print(new_x,new_y)
            self.canvas.coords(self.active, new_x-3, new_y-3, new_x+3, new_y+3)
            label = self.dots[self.canvas.gettags(self.active)[0]]['label']
            self.canvas.coords(label, new_x, new_y - 20)



    def on_dot_release(self, event):
        loc_coords = {}
        for key, dot_dict in self.dots.items():
            dot = dot_dict['dot']
            x, y = self.canvas.coords(dot)[:2]
            loc_coords[key] = (x+3, y+3)
        # print(loc_coords)
        with open("vectors.json", "w", encoding="utf-8") as f:
            json.dump(loc_coords, f, ensure_ascii=False)


# # Load map image
# eelmap = tk.Tk()
# map_img_path = 'lahn2.png'
# map_image = Image.open(map_img_path)
# # map_img = load_map(map_img_path)
# eelmap.geometry("1280x840")  # Set size of root window to 1920x1080 pixels

# # Create a PhotoImage object
# map_photo = ImageTk.PhotoImage(map_image)
# # Create a canvas and add the image to it
# canvas = tk.Canvas(eelmap, width=map_image.width, height=map_image.height)
# canvas.create_image(0, 0, image=map_photo, anchor=tk.NW)
# canvas.pack(fill=tk.BOTH, expand=True)

# locations = Location(canvas, loc_coords)

# # animate(canvas, df)

# # for key, coords in loc_coords.items():
# #     canvas.create_oval(coords[0]-5, coords[1]-5, coords[0]+5, coords[1]+5)

# eelmap.mainloop()

