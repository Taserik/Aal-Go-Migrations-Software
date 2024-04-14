# -*- coding: utf-8 -*-
"""
Created on Tue May  9 18:33:05 2023

@author: TheRickestRick
"""

import json
import pygame as pg
import sys

# Step 1: Load the coordinates from the JSON file and convert them into tuples of integers
with open("locations.json", "r", encoding="utf-8") as f:
    loc_coords = json.load(f)
loc_coords = {k: tuple(int(x) for x in v) for k, v in loc_coords.items()}

# Step 2: Import the animation vectors and store them as a list of tuples of integers
with open("anim_vecs.json", "r", encoding="utf-8") as f:
    anim_vecs = json.load(f)
anim_vecs = [tuple(int(x) for x in vec) for vec in anim_vecs]

# Step 3: Create a list of surfaces to represent each dot, and a list of initial positions for each dot based on the coordinates
pg.init()

screen = pg.display.set_mode((1280, 840))

# Load the background image
bg_img = pg.image.load("lahn2.png")
bg_img = pg.transform.scale(bg_img, (1280, 840))
background = pg.Surface(screen.get_size())
screen.blit(bg_img, (0, 0))

# Define colors
RED = (255, 0, 0)

# Create a list to hold the surfaces for each dot
dot_surfaces = []


for loc in loc_coords.values():
    dot_surface = pg.Surface((10, 10))
    pg.draw.circle(dot_surface, RED, (5, 5), 5)
    dot_surfaces.append(dot_surface)

# Step 5: In the main loop, update the position of each dot based on its progress along the path and blit the dot's surface to the display at its current position.

# Define a variable to keep track of the current frame
frame = 0

# Define a variable to control the speed of the animation
speed = 3

# Create a list to hold the current positions of each dot
dot_positions = list(loc_coords.values())

clock = pg.time.Clock()

# Main loop
while True:
    # Handle user events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    
    # Clear the screen
    screen.blit(background, (0, 0))
    
    # Update the position of each dot based on its progress along the path
    for i, pos in enumerate(dot_positions):
        vec = anim_vecs[i]
        dx, dy = vec[frame % len(vec)]
        new_pos = (pos[0] + dx * speed, pos[1] + dy * speed)
        dot_positions[i] = new_pos
    
    # Blit the dots onto the screen at their current positions
    for i in range(len(dot_surfaces)):
        screen.blit(dot_surfaces[i], dot_positions[i])
    
    # Update the frame
    frame += 1
    
    # Update the screen
    pg.display.update()
    
    # Control the frame rate
    clock.tick(60)



