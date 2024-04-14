import tkinter as tk
import json

# load the location coordinates from a JSON file
with open('locations.json', 'r') as f:
    loc_coords = json.load(f)

# create a dictionary to store the dots as they are created
dots = {}

def on_press(event):
    # create a dot at the initial mouse position
    x, y = event.x, event.y
    dot = canvas.create_oval(x-5, y-5, x+5, y+5, fill='red')
    dots[dot] = (x, y)

def on_drag(event):
    # move the dot as the mouse is dragged
    for dot in dots:
        canvas.move(dot, event.x - dots[dot][0], event.y - dots[dot][1])
        dots[dot] = (event.x, event.y)

def on_release(event):
    # save the new location of the dot to the JSON file
    for dot in dots:
        x, y = dots[dot]
        loc_coords[str(dot)] = {'x': x, 'y': y}
    with open('locations.json', 'w') as f:
        json.dump(loc_coords, f)

# create the root window and canvas
root = tk.Tk()
canvas = tk.Canvas(root)

# set the image as the background of the canvas
img = tk.PhotoImage(file='lahn2.png')
canvas.create_image(0, 0, anchor=tk.NW, image=img)

# create dots for each location in the JSON file
for loc, coords in loc_coords.items():
    x, y = coords['x'], coords['y']
    dot = canvas.create_oval(x-5, y-5, x+5, y+5, fill='red')
    dots[dot] = (x, y)
    canvas.tag_bind(dot, '<Button-1>', lambda e, dot=dot: on_press(e, dot))
    canvas.tag_bind(dot, '<B1-Motion>', on_drag)
    canvas.tag_bind(dot, '<ButtonRelease-1>', on_release)

# pack the canvas and start the event loop
canvas.pack()
root.mainloop()
