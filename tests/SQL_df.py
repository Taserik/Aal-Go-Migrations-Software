#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 23:22:05 2024

@author: tianlin
"""

import sqlite3
import pandas as pd

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('results/mydatabase.db')

# SQL-Abfrage ausführen und Daten in einen DataFrame laden
query = "SELECT * FROM eeltable WHERE rowid BETWEEN 943 AND 967"
df = pd.read_sql_query(query, conn)

# Verbindung zur Datenbank schließen
conn.close()

# Die Daten anzeigen
print(df)