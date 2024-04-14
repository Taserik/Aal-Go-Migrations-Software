#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 16:23:43 2023

@author: erik
"""
import tkinter as tk
from PIL import Image, ImageTk

class MovableImage(tk.Canvas):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.parent = parent
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image, master=self.parent)
        self.map_photo = self.photo  # Assign photo to instance variable
        self.create_image(0, 0, image=self.map_photo, anchor="nw")
        self.bind("<ButtonPress-3>", self.on_button_press)
        self.bind("<B3-Motion>", self.on_move)
        self.bind("<ButtonRelease-3>", self.on_button_release)
        self.bind("<Button-1>", self.canvas_click)  # bind to right-click
        self.canvas_width = self.image.width
        self.canvas_height = self.image.height
        self.last_x = 0
        self.last_y = 0


    def on_button_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_move(self, event):
        self.move("all", event.x - self.last_x, event.y - self.last_y)
        self.last_x = event.x
        self.last_y = event.y

    def on_button_release(self, event):
        pass

    def canvas_click(self, event):
        x, y = event.x, event.y
        tags = self.gettags(self.find_closest(x, y)[0])
        if len(tags) < 4:
            # Clicked outside of dots, do nothing
            return
        loc, pheno, _ = tags[1], tags[2], tags[3]
        show_dataframe(loc, pheno)