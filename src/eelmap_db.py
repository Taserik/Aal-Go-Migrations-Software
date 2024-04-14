#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 09:53:27 2023

@author: erik
"""
import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math
# from tkinter import filedialog
def run():

    mother = pd.read_excel('data/Muttertabelle.xlsx',sheet_name = "Muttertabelle Farben Aale", header = 1, usecols=['ID Code', 'gepunktet', 'Phenotyp', 'Datum', 'Kontrast', 'KF', 'BI', 'OI'], dtype = {'ID Code':str})
    mother.to_pickle('results/motherpickel.pkl')
    # mother = pd.read_pickle('results/motherpickel.pkl')
    mother = mother.rename(columns={'Datum': 'Messdatum'})
    def rm_lead_0(df,col):
        """Entfernt führende Nullen von einer Spalte im Dataframe"""
        ids = df[col].str.lstrip(r'^(0+)')
        df = mother.drop(col, axis=1)
        df.insert(0,col,ids)
        return df
    mother = rm_lead_0(mother,'ID Code')
    # erste Zeile von mother entfernen
    mother = mother.drop(0)
    # den Index um 3 verschieben, um mit Muttertabelle.xlsx zu synchronisieren
    mother.index +=3
    
    # Create a connection to the SQLite database
    conn = sqlite3.connect('results/mydatabase.db')
    
    # Get a cursor for the connection
    id_cursor = conn.cursor()
    
    # Get unique values of ID_HEX from database
    id_cursor.execute('SELECT DISTINCT ID_HEX FROM eeltable')
    
    # Create an empty list to store eel cards
    eelcards = []
    
    # Loop through unique ID_HEX values
    for i in id_cursor.fetchall():
        i = i[0] # extract the ID_HEX value from the tuple
        # Filter mother dataframe for the current ID_HEX value
        eelcard = mother[mother['ID Code'] == i].copy()
    
        # Get unique locations for the current ID_HEX value from the database
        locations_query = f"SELECT DISTINCT Ort FROM eeltable WHERE ID_HEX='{i}'"
        locations = pd.read_sql(locations_query, conn)['Ort'].tolist()
    
        # Get the latest location for the current ID_HEX value from the database
        latest_location_query = f"SELECT Ort FROM eeltable WHERE ID_HEX='{i}' ORDER BY DATUM DESC LIMIT 1"
        latest_location_result = pd.read_sql(latest_location_query, conn)
    
        if not latest_location_result.empty:
            latest_location = latest_location_result['Ort'].iloc[0]
            latest_locations_list = [latest_location]
        else:
            latest_locations_list = []
            latest_location = None
    
        # Create string of locations for each eel
        location_strings = [','.join(locations)]
    
        # Add 'Locations' and 'latest_loc' column to eelcard
        eelcard.loc[:, 'location'] = location_strings
        eelcard.loc[:, 'latest_loc'] = latest_locations_list
    
        # Append eelcard to list of eel cards
        eelcards.append(eelcard)
    
    # Concatenate all eel cards into a single dataframe
    eelcard_df = pd.concat(eelcards, ignore_index=True)
    
    # wander_filtered = wander[wander['is_eel'] == 1]
    def load_map(map_path):
        map_image = Image.open(map_path)
        # map_image = map_image.resize((750,750))
        return ImageTk.PhotoImage(map_image)
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
    
    
    
    # Load map image
    eelmap = tk.Tk()
    map_img_path = 'lahn.png'
    # map_img = load_map(map_img_path)
    eelmap.geometry("1920x1080")  # Set size of root window to 1920x1080 pixels
    canvas = MovableImage(eelmap, map_img_path)
    canvas.image_reference = canvas.image # Keep a reference to the PhotoImage object
    canvas.pack(fill=tk.BOTH, expand=True)
    
        
    # Formatiere die Spalten von Mother, um sie lesbarer zu machen
    mother['KF'] = mother['KF'].astype('float64').round(2)
    mother['BI'] = mother['BI'].astype('float64').round(2)
    mother['OI'] = mother['OI'].astype('float64').round(2)
    mother['Messdatum'] = pd.to_datetime(mother['Messdatum'])
    mother['Messdatum'] = mother['Messdatum'].dt.date
    mother['Messdatum'] = mother['Messdatum'].apply(lambda x: x.strftime('%d-%m-%Y') if not pd.isna(x) else '')
    
    # create a dictionary to map locations to their coordinates
    location_coordinates = {'LÖHN_OW': (1340, 35), 'LÖHN_UW': (1300, 100), 'WEIL_OW': (1308, 140), 'WEIL_UW': (1275, 155), 
                            'KIRS_OW': (1225, 215), 'KIRS_UW': (1230, 260), 'FÜRF_OW': (1250, 395), 'FÜRF_UW': (1255, 440), 
                            'VILL_OW': (1075, 550), 'VILL_UW': (1070, 580), 'RUNK_OW': (1000,540), 'RUNK_UW': (950,540), 
                            'LIMB_OW': (810,570), 'LIMB_UW': (690,570), 'DIEZ_OW': (535,640), 'DIEZ_UW': (550,685), 
                            'CRAM_OW': (305,815), 'CRAM_UW': (340,840), 'KALK_OW': (258,950), 'KALK_UW': (225,925)}
    
    # strip dataframe from all whitespaces
    eelcard_df = eelcard_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    rangequery = "SELECT ID_HEX, Ort, Min(DATUM) AS min_date, MAX(DATUM) AS max_date FROM eeltable GROUP BY ID_HEX, Ort"
    
    # Apply the date_range function to the "Date" column of the grouped dataframe
    date_ranges = pd.read_sql(rangequery, conn)
    
    # define a function to show the date range for each location and eel
    def show_date_range():
           # create a new window to display the dataframe
        new_window = tk.Toplevel(eelmap)
        new_window.geometry('1000x700')
        
        # create a treeview widget to display the dataframe
        treeview = ttk.Treeview(new_window)
        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # add columns to the treeview
        treeview["columns"] = date_ranges.columns.tolist()
        for col in treeview["columns"]:
            treeview.heading(col, text=col)
        
        # insert data into the treeview
        for i, row in date_ranges.iterrows():
            values = row.tolist()
            treeview.insert("", tk.END, text=i, values=values)
    
    # add a button to show date range information
    date_range_button = tk.Button(eelmap, text="Zeige Wanderdaten", command=show_date_range)
    date_range_button.pack(side=tk.TOP, padx=10, pady=10)
    
    conn.close()
    
    
    def canvas_click(event):
        x, y = event.x, event.y
        tags = event.widget.find_closest(x, y)
        if not tags:
            # Clicked outside of dots, do nothing
            return
        tags = event.widget.gettags(tags[0])
        if len(tags) < 4:
            # Clicked outside of dots, do nothing
            return
        loc, pheno, _ = tags[1], tags[2], tags[3]
        show_dataframe(loc, pheno)
    
    
    # Group by latest_loc and count the number of each phenotype
    phenotype_counts = eelcard_df.groupby(['latest_loc', 'Phenotyp']).size().reset_index(name='count')
    
    # Create circles on canvas based on count of each phenotype
    dot_offsets = {}  # Dictionary to store the x and y offsets for each dot
    for loc, pheno, count in phenotype_counts[['latest_loc', 'Phenotyp', 'count']].values:
        x, y = location_coordinates[loc]
        radius = math.sqrt(count) * 5
        offset_x, offset_y = dot_offsets.get((x, y), (1, 1))  # Get any existing offset for this location
        if pheno == 'B':
            fill_color = 'white'
            dot_id = canvas.create_oval(x - radius + offset_x, y - radius + offset_y, x + radius + offset_x, y + radius + offset_y, fill=fill_color, tags=('dot', loc, pheno, count))
        elif pheno == 'G':
            fill_color = 'yellow'
            dot_id = canvas.create_oval(x - radius + offset_x, y - radius + offset_y, x + radius + offset_x, y + radius + offset_y, fill=fill_color, tags=('dot', loc, pheno, count))
        elif pheno == 'I':
            fill_color = 'orange'
            dot_id = canvas.create_oval(x - radius + offset_x, y - radius + offset_y, x + radius + offset_x, y + radius + offset_y, fill=fill_color, tags=('dot', loc, pheno, count))
        # Update the offset for this location based on the size of the dot
        dot_offsets[(x, y)] = (offset_x + radius * 1, offset_y)
    
        # # Get the coordinates of the first and second dots on the canvas
        # dot1_coords = canvas.coords(canvas.find_withtag('dot')[0])
        # dot2_coords = canvas.coords(canvas.find_withtag('dot')[1])
        
        # # Set the initial position of the circle to the coordinates of the first dot
        # x1, y1 = dot1_coords[0], dot1_coords[1]
        
        # # Set the final position of the circle to the coordinates of the second dot
        # x2, y2 = dot2_coords[0], dot2_coords[1]
        
        # # Create a blue circle at the initial position
        # r = 10
        # circle = canvas.create_oval(x1-r, y1-r, x1+r, y1+r, fill='blue')
    
        # # Calculate the step size for x and y
        # dx = (x2-x1)/20.0
        # dy = (y2-y1)/20.0
    
        # # Define a function to move the circle
        # def move_circle():
        #     global dx, dy
        #     canvas.move(circle, dx, dy)
        #     # If the circle has not reached the final position yet, call this function again after a short delay
        #     if ((x2-x)**2 + (y2-y)**2)**0.5 > r:
        #         canvas.after(100, move_circle)
                
        # move_circle()
    
    
    
    
        # Bind the <Enter> and <Leave> events to the dot
        canvas.tag_bind(dot_id, "<Enter>", lambda event, dot_id=dot_id: show_info(dot_id))
        # canvas.tag_bind(dot_id, "<Button-1>", lambda event, loc=loc: show_dataframe(loc))
        # canvas.bind("<Button-1>", canvas_click)
    
    def show_dataframe(loc, pheno):
        # Filter the dataframe based on loc and pheno
        filtered_df = eelcard_df[(eelcard_df['latest_loc'] == loc) & (eelcard_df['Phenotyp'] == pheno)]
    
        # Calculate the height of the window based on the number of rows
        row_height = 20  # Change this value if needed
        num_rows = len(filtered_df.index)
        window_height = 50 + num_rows * row_height  # Add some padding to the height
    
        # Create a new window with the calculated height
        window = tk.Toplevel(eelmap)
        window.geometry("1000x{}".format(window_height))
        window.title("all_eelcards dataframe")
    
        # Create a scrollbar for the treeview
        scrollbar = tk.Scrollbar(window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
        # Create a treeview to display the dataframe
        treeview = ttk.Treeview(window, yscrollcommand=scrollbar.set)
        treeview.pack(side=tk.LEFT, fill=tk.BOTH)
    
        # Configure the columns of the treeview
        columns = list(filtered_df.columns)
        treeview["columns"] = columns
        treeview.column("#0", width=0, stretch=tk.NO)
        for column in columns:
            treeview.column(column, width=100, anchor=tk.CENTER)
            treeview.heading(column, text=column, anchor=tk.CENTER)
    
        # Insert the filtered dataframe into the treeview
        for values in filtered_df.values:
            treeview.insert("", tk.END, values=tuple(values))
    
        # Configure the scrollbar to scroll the treeview
        scrollbar.config(command=treeview.yview)
    
        # Add tag configuration for highlighting
        treeview.tag_configure("highlight", background="yellow")
    
        # Wait until the window is displayed before grabbing it
        window.update_idletasks()
        window.grab_set()
    
        
    def show_info(dot_id):
        # Get the location, phenotype, and count information from the dot's tags
        tags = canvas.itemcget(dot_id, "tags").split()
        # phenotype = tags[2]
        count = tags[3]
    
        # Create a tooltip label with the phenotype count information
        tooltip_label = tk.Label(canvas, text=f"{count}", font= ('Helvetica',16), bd=0, highlightthickness=0)
        # Get the coordinates of the dot and adjust the tooltip position to be just above the dot
        x1, y1, x2, y2 = canvas.coords(dot_id)
        tooltip_x = x1 + (x2 - x1) / 2
        tooltip_y = y1 - 20
    
        # Add the tooltip label to the canvas and adjust its position
        tooltip_id = canvas.create_window(tooltip_x, tooltip_y, window=tooltip_label, anchor="center")
    
        # Bind the <Leave> event to the tooltip label so it disappears when the mouse leaves the dot
        canvas.tag_bind(dot_id, "<Leave>", lambda event: canvas.delete(tooltip_id))
    
    eelmap.mainloop()

run()