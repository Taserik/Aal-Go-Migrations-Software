# -*- coding: utf-8 -*-
"""
Created on Fri May 26 14:46:48 2023

@author: TheRickestRick
"""

import tkinter as tk
import time

root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

# Create two rectangles
rectangle1 = canvas.create_rectangle(0, 0, 50, 50, fill='blue')
rectangle2 = canvas.create_rectangle(150, 150 , 200, 200, fill='red')

path = [(10,60),(20,70),(30,80),(40,90),(50,100),(60,110),(70,120),(80,130),(90,140),(100,150)]

# Get actual canvas width
canvas_width = canvas.winfo_reqwidth()
canvas_height = canvas.winfo_reqheight()

# Animation using move method
def animate_move():
    x1, y1, x2, y2 = canvas.coords(rectangle1)
    
    canvas.move(rectangle1, 1, 0)
    recmove = canvas.after(20, animate_move)  # Schedule the next movement
    # If the line has reached the end of the timeline, reset its position to the left
    if x2 >= canvas_width:
        canvas.after_cancel(recmove)
# Animation using canvas.coords method
def animate_coords(index=0):
    if index < len(path):
        x1, y1 = path[index]
        canvas.coords(rectangle2, x1+50, y1+50, x1, y1)
        canvas.after(1000, animate_coords, index + 1)  # Schedule the next movement

    # If the line has reached the end of the timeline, reset its position to the left
    # if x1 <= 50:
    #     canvas.after_cancel(recmove2)
# Start both animations
animate_move()

animate_coords()

root.mainloop()
