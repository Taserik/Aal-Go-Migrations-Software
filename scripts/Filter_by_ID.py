# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 17:41:18 2023

@author: TheRickestRick
"""

import pandas as pd

# Lese Excel-Tabelle "Muttertabelle Farben Aale" der Muttertabelle 
# als Dataframe ein, nehme Zeile 3 als Header

# df = pd.read_excel(r'C:\Users\Anna-Lena\Nextcloud\Farbmessung Aale\Farbmessung Aale\Erik\Muttertabelle.xlsx',sheet_name = "Muttertabelle Farben Aale", header = 2)
                    

# nur für Testzwecke
# df.to_pickle("filter_by_id.pk1")
df = pd.read_pickle("filter_by_id.pk1")

# Schreibe ID-Code Spalte als Series-Object in Variable

mother_ids = df["ID Code"]


# Liste der protokollierten Nummern in Variable schreiben, startet mit 1
sheetindex = 1
# Listen zum späteren Anhängen an Datei
location = []
indsheet = []
sheetnames = pd.ExcelFile(r'C:/Users/Anna-Lena/Nextcloud/Farbmessung Aale/Erik/ID_Codes_Migromat.xlsx').sheet_names
# Erstelle Liste mit Indexen der eingelesenen Liste "sheetnames"
indexes = []
for index in range(len(sheetnames)):
    indexes.append(index)


for length in range(len(sheetnames)):
    
    # Input-Datei einlesen und im Dataframe Spalten beschriften        
     idframe = pd.read_excel(r'C:/Users/Anna-Lena/Nextcloud/Farbmessung Aale/Erik/ID_Codes_Migromat.xlsx',sheet_name = sheetnames[length])
     idframe.columns = ['ids', 'Datum', 'Uhrzeit']
     idframe = idframe.drop_duplicates(subset = ['ids']).reset_index(drop = True)
     #Series Object in Variable schreiben
     idseries = idframe['ids']
   
       
    # except ValueError:
    #     continue
        
# finde ID's in Muttertabelle und schreibe Index der Muttertabelle in Liste    
     for i in range (0,len(idseries)): 
        try:
            loc = mother_ids[mother_ids == idseries[i]].index
            loc = int(loc[0])    
            # print(loc + 4, ' -', sheetindex, '-', table - 1)
            location.append(loc+4)
            indsheet.append(sheetindex)
            sheetindex += 1
            
# Ist der Testsender '00074ED317' vorhanden, schreibe ihn
# schreibe "checknum", wenn die ID nicht in Muttertabelle vorkommt
        except IndexError:
            if idseries[i] == '00074ED317':
                location.append('Testsender')
                indsheet.append('n/a')                
            else:
                location.append('Nummer prüfen')
                indsheet.append('n/a')
                sheetindex += 1
        # try:
     if length == 0:
        idframe.insert(3, 'Loc in Muttertabelle', location)
        idframe.insert(4,'ID auf Protokoll', indsheet)
        # Erstelle Datei im .xlsx Format
        with pd.ExcelWriter(r'C:/Users/Anna-Lena/Nextcloud/Farbmessung Aale/Erik/ID_output.xlsx') as writer:
            idframe.to_excel(writer, sheet_name = sheetnames[length], index = False)
        # Wenn ein neues Tabellenblatt angefangen wird, resette den laufenden 
        #Index und leere die Listen
        sheetindex = 1
        indsheet= []
        location = []      
     elif length in indexes[1:]:
        idframe.insert(3, 'Loc in Muttertabelle', location)
        idframe.insert(4,'ID auf Protokoll', indsheet)
        # Hänge an eben erstellte Datei an
        with pd.ExcelWriter(r'C:/Users/Anna-Lena/Nextcloud/Farbmessung Aale/Erik/ID_output.xlsx', mode="a", engine="openpyxl") as writer:
            idframe.to_excel(writer, sheet_name = sheetnames[length], index = False)
        sheetindex = 1
        indsheet= []
        location = []            
        
