# -*- coding: utf-8 -*-
"""
Created on Tue May  9 17:45:52 2023

@author: TheRickestRick
"""
import pygame as pg
import json
import sys
import os

# Define the list of tuples of the coordinates you want the animation to be in
with open("locations.json", "r", encoding="utf-8") as f:
    loc_coords = json.load(f)

with open("anim_vecs.json", "r", encoding="utf-8") as f:
    coords = json.load(f)


# Initialize Pygame
pg.init()

# Set up the Pygame display
screen = pg.display.set_mode((1280, 840))
img_path = 'lahn2.png'
abs_path = os.path.abspath(img_path)
background_img = pg.image.load(img_path).convert()

# Create a surface for the background image
background = pg.Surface(screen.get_size())
background.blit(background_img, (0, 0))

# Define colors
RED = (255, 0, 0)

# Create a list to hold the surfaces for each dot
dot_surfaces = []
dot_positions = []

# For each dot, create a surface with a yellow circle on it at the starting position
for x, y in loc_coords:
    dot_surface = pg.Surface((10, 10))
    dot_surface.fill((255, 255, 255))
    pg.draw.circle(dot_surface, RED, (5, 5), 5)
    dot_rect = dot_surface.get_rect(center=(x, y))
    dot_surfaces.append(dot_surface)
    dot_positions.append((x, y))

# Set up the clock for controlling the frame rate
clock = pg.time.Clock()

# Define the speed of the dots
dot_speed = 2

# Define the index of the current position of the dot
dot_index = 0

# Main Pygame loop
while True:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    # Update the position of the dot
    x, y = dot_positions[dot_index]
    next_x, next_y = loc_coords[dot_index + 1]
    distance = ((next_x - x) ** 2 + (next_y - y) ** 2) ** 0.5
    if distance < dot_speed:
        dot_index += 1
        if dot_index >= len(loc_coords) - 1:
            dot_index = 0
    else:
        dx = dot_speed * (next_x - x) / distance
        dy = dot_speed * (next_y - y) / distance
        dot_positions[dot_index] = (x + dx, y + dy)

    # Blit the background onto the screen
    screen.blit(background, (0, 0))

    # Draw the dots on the Pygame display
    for dot_surface, (x, y) in zip(dot_surfaces, dot_positions):
        dot_rect = dot_surface.get_rect(center=(x, y))
        screen.blit(dot_surface, dot_rect)

    # Update the Pygame display
    pg.display.update()

    # Limit the frame rate
    clock.tick(60)
