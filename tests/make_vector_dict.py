#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  5 17:58:53 2023

@author: erik
"""

import json

coordinates = {}
for i in range(1, 121):
    if i <= 10:
        x = 200 + i*20
        y = 200
    elif i <= 20:
        x = i*20
        y = 250
    elif i <= 30:
        x = -200 + i*20
        y = 300
    elif i <= 40:
        x = -400 + i* 20
        y = 350
    elif i <= 50:
        x = -600 + i*20
        y = 400
    elif i <= 60:
        x = -800 + i*20
        y = 450
    elif i <= 70:
        x = -1000 + i*20
        y = 500
    elif i <= 80:
        x = -1200 + i*20
        y = 550
    elif i <= 90:
        x = -1400 + i*20
        y = 600
    elif i <= 100:
        x = -1600 + i*20
        y = 650
    elif i <= 110:
        x = -1800 + i*20
        y = 700
    else:
        x = -2000 + i*20
        y = 750
    coordinates[str(i)] = [x, y]

print(coordinates)

with open("vectors.json", "w", encoding="utf-8") as f:
    json.dump(coordinates, f, ensure_ascii=False)