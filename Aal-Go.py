# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:38:34 2023

@author: TheRickestRick
"""

# Importiere die benötigten Module

import pandas as pd
import datetime as dt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.load_image import load_image
import sys
from src.rotating_image import RotatingImage
import sqlite3

# create a dictionary to map locations to their coordinates
location_coordinates = {'LÖHN_OW': (1340, 35), 'LÖHN_UW': (1300, 100), 'WEIL_OW': (1308, 140), 'WEIL_UW': (1275, 155), 
                        'KIRS_OW': (1225, 215), 'KIRS_UW': (1230, 260), 'FÜRF_OW': (1250, 395), 'FÜRF_UW': (1255, 440), 
                        'VILL_OW': (1075, 550), 'VILL_UW': (1070, 580), 'RUNK_OW': (1000,540), 'RUNK_UW': (950,540), 
                        'LIMB_OW': (810,570), 'LIMB_UW': (690,570), 'DIEZ_OW': (535,640), 'DIEZ_UW': (550,685), 
                        'CRAM_OW': (305,815), 'CRAM_UW': (340,840), 'KALK_OW': (258,950), 'KALK_UW': (225,925)}

after_filein = False

root = tk.Tk()

# Formatierung der GUI
root.title("Eelpaths")
root.geometry("540x240")
bg = load_image("background.png")
image_label = tk.Label(root, image = bg)
image_label.place(x=0, y=2, relwidth=1, relheight=1)

# define function to open the map window
def open_map():
    import src.eelmap_db
    src.eelmap_db.run()
    
map_button = tk.Button(root, text="Karte öffnen", command=open_map)
map_button.grid(row = 5,column=0)

# Fenster zur Findung der Datei öffnet sich
def filein():
    root.fileinput = filedialog.askopenfilename(initialdir = "C:/Users/TheRickestRick/Desktop/Denoiser_3/Data_Mrz_22", title="Wähle eine Datei.", filetypes=(("csv files","*.csv"),("Alle Dateien","*.*")))

    # Einlesen von .CSV Rohdaten mit Benennung der Spalten und Festlegung der 
    # Datentypen für spätere Bearbeitung
    
    global df
    global after_filein
    after_filein = True
    # Read only the first row of the file
    with open(root.fileinput, 'r') as f:
        first_row = f.readline()
    
    # Count the number of commas in the first row to determine the number of columns
    num_columns = first_row.count(',') + 1
    
    # Define column names based on the number of columns
    # Read the entire file with the determined number of columns and column names
    if num_columns == 4:
        column_names = ['Serial_XLDate', 'Frac_Sec', 'ID', 'POWER']
        df = pd.read_csv(root.fileinput, names=column_names, dtype = {'Serial_XLDate' : float,'ID': str}).drop_duplicates(subset=['Serial_XLDate','ID']).reset_index(drop = True)
        if any(df['ID'].str.contains('[a-fA-F]')):
            # ID column contains at least one hexadecimal number, convert to decimal and assign to ID_Dec column
            df['ID_Dec'] = df['ID'].apply(lambda x: str(int(x, 16)))
            # drop the original ID column
            df = df.drop('ID', axis=1)
        else:
            # ID column does not contain any alphabetical letters, so assume it only has decimal values and assign to ID_Dec column
            df['ID_Dec'] = df['ID']
            df['ID_HEX'] = df['ID'].apply(lambda x: hex(int(x))[2:].upper())
            df = df.drop('ID', axis=1)

    elif num_columns == 5:
        column_names = ['Serial_XLDate', 'Frac_Sec', 'ID1', 'ID2', 'POWER']
        df = pd.read_csv(root.fileinput, names=column_names, dtype = {'Serial_XLDate' : float,'ID1':str,'ID2':str}).drop_duplicates(subset=['Serial_XLDate','ID1']).reset_index(drop = True)
        if any(df['ID1'].str.contains('[a-fA-F]')):
            # ID1 column contains at least one hexadecimal number, convert to decimal and assign to ID_HEX column
            df['ID_Dec'] = df['ID2']
            df['ID_HEX'] = df ['ID1']
            df = df.drop(['DF1','DF2'], axis=1)
        else:
            df['ID_Dec'] = df['ID1']
            df['ID_HEX'] = df ['ID2']
            df = df.drop(['ID1','ID2'], axis=1)
    
    #Debug-Ausgabe Zeilenanzahl vor Filtrierung
    print("Number of rows:", len(df))
    # df = df.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
    global filein_label
    var.set('Datei eingelesen')
    filein_label.config(fg = "green")
   
button_filein=tk.Button(root, text="Datei öffnen", command=filein)
button_filein.grid(row=0, column=0, padx=25, pady=8)


#Labels auf GUI-Grid platzieren und benennen

var = tk.StringVar()
var.set('Datei nicht eingelesen!')

filein_label = tk.Label(root, textvariable = var, fg="red")    
filein_label.grid(row=0, column=1, pady=8)
ort_label = tk.Label(root, text = "Ort")
ort_label.grid(row=1, column = 0,pady=8)
receiver_label = tk.Label(root, text = "Receiver")
receiver_label.grid(row = 2, column = 0,pady=8)
timetol_label = tk.Label(root, text = "Zeit-Toleranz in s")
timetol_label.grid(row=3,column=0,pady=8)
dist_label = tk.Label(root, text="Zeit-delta-3 in s")
dist_label.grid(row=4,column=0,pady=8)

options =["0 : keine Angabe gemacht",
"1 : LÖHN_OW",
"2 : LÖHN_UW",
"3 : WEIL_OW",
"4 : WEIL_UW",
"5 : KIRS_OW",
"6 : KIRS_UW",
"7 : FÜRF_OW",
"8 : FÜRF_UW",
"9 : VILL_OW",
"10 : VILL_UW",
"11 : RUNK_OW",
"12 : RUNK_UW",
"13 : LIMB_OW",
"14 : LIMB_UW",
"15 : DIEZ_OW",
"16 : DIEZ_UW",
"17 : CRAM_OW",
"18 : CRAM_UW",
"19 : KALK_OW",
"20 : KALK_UW"
]

# Die Zeiten, die als Aalsignal akzeptiert werden als List of Strings für
# Combobox
time_tolerance = ["5-19","5-25","5-31","5-37"]

ort_combobox = ttk.Combobox(root, value = options)
ort_combobox.current(0)
ort_combobox.grid(row=1, column = 1)

receiver_entry = tk.Entry(root)
receiver_entry.grid(row=2, column = 1)

timetol_combobox = ttk.Combobox(root, value = time_tolerance)
timetol_combobox.current(0)
timetol_combobox.grid(row = 3, column =1)

dist_spinbox = ttk.Spinbox(root,from_= 20, to = 100)
dist_spinbox.set(60)
dist_spinbox.grid(row=4, column=1)

# Listen, die über ok-Funktion mit ausgewählten Elementen gefüllt werden
orte = []
ortnr = []
timetol = []
receiver = []

def noisefilter():
    """Filtert Rohdaten, erkennt Aalsignale(z.B. alle 5,6,7,11,12,13,17,18,19 sek) und speichert diese 
    in einer sql-database 'mydatabase.sql' oder nach alter Version in einer Exceldatei 'Hydrophondaten.xlsx'"""
    global df
    # Sortiere Dataframe in sinnvoller Reihenfolge
    df = df[['ID_Dec','ID_HEX','Frac_Sec','POWER','Serial_XLDate']]
    
    # datexl ist ein Series Object, in dem Zeitstempel im numerischen Format
    # abgespeichert werden. Excel bezieht sich bei diesen sogenannten "Serial
    # Numbers" auf das Datum 01-01-1900 und zählt von dort aus in Tagen hoch
    
    datexl = df["Serial_XLDate"]
        
    
    # Die Tage zwischen Excel und Python waren um zwei verschoben, weshalb hier
    # auf das Datum 30-12-1899 korrigiert wurde, um richtige Ergebnisse zu erhalten
    
    def xldate_to_datetime(xldate):
        '''Konvertiert ein Datum von Serial Number von Excel zu eigentlichem Datum'''
        temp = dt.datetime(1899, 12, 30)
        delta = dt.timedelta(days=xldate)
        return temp+delta
    def round_seconds(obj: dt.datetime) -> dt.datetime:
        """Rundet ein Datetime.Object auf Sekunden Genauigkeit"""
        if obj.microsecond >= 500_000:
            obj += dt.timedelta(seconds=1)
        return obj.replace(microsecond=0)
    
    # leere Liste für Daten, die als str gespeichert werden
    time = []
    
    # Fülle Liste mit auf Sekunden gerundete Daten
    for d in datexl:
        round_date = round_seconds(xldate_to_datetime(d))
        time.append(round_date)
    
    # Hänge Listen Datum, Receiver, Ort und Nr. an Dataframe
    df.insert(0, "Nr", ortnr)
    df.insert(1, "Ort", orte)
    df.insert(2, "DATUM", time)
    df.insert(5, "Receiver", receiver)
    
    # Speichere Index des letzten aufgerufenen Aals als Startpunkt
    last_eel = 0
    
    # Der Index von Datum und ID_HEX muss ebenfalls als Startpunkt gespeichert werden
    comp_var = 2
    
    # leere Liste für Aalsignal "Ja" = 1 oder "Nein" = 0
    is_eel = []
    
    # Daten, die verglichen werden sollen, in Series Object schreiben
    
    date = df['DATUM']
    
    eel_id = df['ID_HEX']
    
    
    # Mit range(1, len(date)) erzeuge ich eine ganzzahl Liste von 1 bis zur 
    # maximalen größe der Spalte
    for i in range(1,len(date)):
        if comp_var == len(date):
            break
       
        # Die Distanz zweier aufeinanderfolgender Zeitpunkte in Sekunden(86400 s/d)
        distance = round(((abs(datexl.iloc[i]-datexl.iloc[last_eel]))*86400))
        
        # Die Distanz zwischen drei Zeitpunkten in Sekunden
        distance3 = round(((abs(datexl.iloc[comp_var]-datexl.iloc[last_eel]))*86400))
        
        if date.iloc[i-1].date() == date.iloc[comp_var].date() and date.iloc[i].date() == date.iloc[comp_var].date() and eel_id.iloc[i-1] == eel_id.iloc[comp_var] and eel_id.iloc[i] == eel_id.iloc[comp_var] and distance >= 5 and distance in timetol and distance3 <= distance_tolerance:
            # ist ein Aal-Signal
            is_eel.append(1)
        else:
            # Sonst falsch
            is_eel.append(None)
        last_eel = i
        comp_var = i+2
    df.drop(df.tail(2).index, inplace=True)
    df.insert(4, 'is_eel' ,is_eel, allow_duplicates = True)
    df = df.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
    df_filtered = df[df['is_eel']==1].drop(['Nr','ID_Dec','Receiver','is_eel','Frac_Sec','POWER'],axis=1)
    if len(df_filtered) > 0:
        df_filtered['x_coordinate'] = df_filtered['Ort'].apply(lambda x: location_coordinates[x][0])
        df_filtered['y_coordinate'] = df_filtered['Ort'].apply(lambda x: location_coordinates[x][1])
    else:
        messagebox.showerror("Error","kein valides Aalsignal in den Daten")
   # Debug-Ausgabe der Zeilenanzahl nach Filtrierung
    print("Number of rows:", len(df_filtered))

    try:
        # with pd.ExcelWriter(r'out.xlsx', mode="a", engine="openpyxl",if_sheet_exists = "overlay") as writer:
        #     df.to_excel(writer,sheet_name = 'Hydrophondaten',startrow=writer.sheets['Hydrophondaten'].max_row,index = False, header=False)
        # with pd.ExcelWriter(r'out_is_eel.csv', mode="a", engine="openpyxl",if_sheet_exists = "overlay") as writer:
        #     df_filtered.to_excel(writer,sheet_name = 'Hydrophondaten',startrow=writer.sheets['Hydrophondaten'].max_row,index = False, header=False)
       # Create a connection to the SQLite database
        conn = sqlite3.connect('results/mydatabase.db')
        # Write the dataframe to a table in the SQLite database
        df_filtered.to_sql('eeltable', conn, if_exists='append',index = False)
    except:
        # with pd.ExcelWriter(r'out.xlsx', mode="w", engine="openpyxl") as writer:
        #     df.to_excel(writer,sheet_name = 'Hydrophondaten',index = False, header=True)
        # with pd.ExcelWriter(r'out_is_eel.csv', mode="w", engine="openpyxl") as writer:
        #     df_filtered.to_excel(writer,sheet_name = 'Hydrophondaten',index = False, header=True)
        df_filtered.to_sql('eeltable', conn, if_exists='replace',index = False)
      



def ok():
    """Führt bei Klicken des Ok-Buttons alle Einstellungen aus und übergibt
    sie an Listen oder Variablen"""
    
    # behandle after_filein als globale Variable
    global after_filein
    global orte
    global ortnr
    global receiver
    if after_filein == True and ort_combobox.get() != "0 : keine Angabe gemacht" and receiver_entry.get() != "":
        # nach einem mal Drücken des ok-Button wird dieser deaktiviert.
        def do_nothing():
            pass
        button['command']= do_nothing
        # Hänge Orte und Receiver an Liste und schreibe Ort, zugehörige Nummer 
        # und Receiver so oft in eine Liste, wie es 
        # Einträge in der Spalte des dataframes gibt
        orte.append(ort_combobox.get()[4:])
        ortnr.append(ort_combobox.get()[:2].replace(" ",""))
        receiver.append(receiver_entry.get())
        orte = orte*len(df['ID_HEX'])
        ortnr = ortnr*len(df['ID_HEX'])
        receiver = receiver*len(df['ID_HEX'])
        # Schreibe Distanz-Toleranz in globale Variable
        global distance_tolerance
        distance_tolerance = int(dist_spinbox.get())
        # Schreibe je nach Auswahl Liste der Zeittoleranzen in timetol
        if timetol_combobox.get() == "5-19":
            timetol.extend([5,6,7,11,12,13,17,18,19])
        elif timetol_combobox.get() == "5-25":
            timetol.extend([5,6,7,11,12,13,17,18,19,23,24,25])
        elif timetol_combobox.get() == "5-31":
            timetol.extend([5,6,7,11,12,13,17,18,19,23,24,25,29,30,31])
        elif timetol_combobox.get() == "5-37":
            timetol.extend([5,6,7,11,12,13,17,18,19,23,24,25,29,30,31,35,36,37])
        # starte Animation
        rotating_image.start_rotation()
        noisefilter()
        root.after(1500, root.destroy)
        # Zerstöre das Fenster und führe restlichen Code aus
        # root.destroy()
    elif after_filein == 0:
        messagebox.showerror("Keine Datei eingelesen", "Die Datei wurde noch nicht eingelesen.")
    elif ort_combobox.get() == "0 : keine Angabe gemacht" and receiver_entry.get() == "":
        messagebox.showerror("Ort und Receiver fehlen", "Bitte einen Ort und einen Receiver angeben.")
    elif ort_combobox.get() == "0 : keine Angabe gemacht":
        messagebox.showerror("Ort fehlt", "Bitte einen Ort angeben.")
    elif receiver_entry.get() == "":
        messagebox.showerror("Receiver fehlt", "Bitte einen Receiver angeben.")

        
        
# Der ok-Button, der bei Klick die ok-Funktion ausführt     
buttpic = tk.PhotoImage(file="eel.png")  
button = tk.Button(root, text="OK", command=ok, image=buttpic, compound='center',width = 50, height=50)
rotating_image = RotatingImage(root, button, 'eel.png')
button.grid(row = 5, column=1)

def on_closing():
    """Was passiert beim Verlassen des Programms über 'X'"""
    if messagebox.askokcancel("Quit", "Willst du das Programm verlassen?"):
        root.destroy()
        # Unterbreche das weitere Programm
        sys.exit()
        
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

        
