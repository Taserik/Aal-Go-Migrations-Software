#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 12:07:05 2024

@author: tianlin
"""

import sqlite3
import tkinter as tk
from src.load_image import load_image
from tkinter import filedialog, messagebox, simpledialog
import Denoiser3
import pandas as pd

root = tk.Tk()
# Formatierung der GUI
root.title("Eelpaths")
root.geometry("540x240")
bg = load_image("background.png")
image_label = tk.Label(root, image = bg)
image_label.place(x=0, y=2, relwidth=1, relheight=1)

def conn_database():
    """Verbindet sich mit der Database oder erstellt eine neue Datenbank"""
    # Öffne Dialogfenster zum Einlesen der Datenbank
    root.fileinput1 = filedialog.askopenfilename(initialdir = "C:/)", title="Wähle eine Datei.", filetypes=(("db files","*.db"),("Alle Dateien","*.*")))
    try:
        connection = sqlite3.connect(root.fileinput1)
        messagebox.showinfo("Erfolg", "Datenbank erfolgreich eingelesen.")
        return connection
    except sqlite3.Error as e:
        messagebox.showerror("Fehler beim einlesen der Datenbank.",e)
def new_database():
    """Erstellt eine neue Datenbank"""
    new_data = simpledialog.askstring("Dateiname", "Geben Sie der Datenbank einen Namen ohne Dateiwerweiterung:")
    if new_data:
        new_data += ".db"
        print("Eingabe:", new_data)  # Debugging-Ausgabe
        
        # Überprüfe, ob der Dateiname gültig ist
        if not all(c.isalnum() or c in ['_', '-', '.', ' '] for c in new_data):
            raise ValueError("Ungültiger Dateiname. Verwenden Sie nur alphanumerische Zeichen, Bindestriche, Unterstriche oder Leerzeichen.")
        
        connection = sqlite3.connect(new_data)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS eeltable (
                   Ort TEXT,
                   Datum TIMESTAMP,
                   ID_HEX TEXT,
                   Serial_XLDate FLOAT,
                   x_coordinate INTEGER,
                   y_coordinate INTEGER
               )''')


        connection.commit()  # Änderungen an der Datenbank speichern
        messagebox.showinfo("Erfolg", "Datenbank erfolgreich erstellt.")
    else:
        messagebox.showerror("Fehler", "Bitte geben Sie einen Namen für die Datenbank ein.")
    return connection
    root.destroy()
    Denoiser3.main()        

# Button, um sich mit Database zu verbinden
button1 = tk.Button(root, text="neue Datenbank", command=new_database,width = 17, height=5)
button1.pack(side="top", anchor="nw", pady=10, padx=10)  # Zentrieren des ersten Buttons

button2 = tk.Button(root, text="Datenbank auswählen", command=conn_database,width = 17, height=5)
button2.pack(side="top", anchor="sw", pady=10, padx=10)  # Zentrieren des zweiten Buttons

root.mainloop()