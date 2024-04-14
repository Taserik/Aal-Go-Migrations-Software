#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 13:20:46 2024

@author: tianlin
"""

from PIL import Image, ImageTk

def load_image(image):
    img = Image.open(image)  # Open the image file
    img_ref = ImageTk.PhotoImage(img)  # Convert the image for tkinter
    return img_ref