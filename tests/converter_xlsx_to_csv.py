#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 07:40:50 2024

@author: tianlin
"""

import os
import pandas as pd
import csv

# Define the directory containing the .xlsx files
directory = '/home/tianlin/Dropbox/Thesis/Denoiser_3/data/Data_Okt_Dez_2022'

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
        # Read the Excel file and skip the first row
        df = pd.read_excel(os.path.join(directory, filename), header=None)
        
        df = df.iloc[:,0]
        
        # Define the output file path (change extension to .csv)
        output_filename = os.path.splitext(filename)[0] + '.csv'
        output_path = os.path.join(directory, output_filename)
        
        # Save the DataFrame to a .csv file with an escape character
        df.to_csv(output_path, index=False, header=False, quoting=csv.QUOTE_NONE, escapechar=' ')

        print(f"{filename} converted to {output_filename}")





