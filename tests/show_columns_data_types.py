#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 13:32:35 2024

@author: tianlin
"""

import sqlite3

def view_column_data_types(database_path, table_name):
    try:
        # Establish connection to the database
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Execute SQL query to retrieve column names and data types
        cursor.execute(f"PRAGMA table_info({table_name})")

        # Fetch all rows from the cursor
        rows = cursor.fetchall()

        # Print column names and data types
        print("Column Name\tData Type")
        for row in rows:
            print(row[1], "\t\t", row[2])

        # Close cursor and connection
        cursor.close()
        connection.close()

    except sqlite3.Error as e:
        print("Error:", e)

# Assuming 'database_path' is the path to your SQLite database file and 'eeltable' is the table name
view_column_data_types('../results/mydatabase.db', "eeltable")
