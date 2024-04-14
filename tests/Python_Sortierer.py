# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 13:56:28 2023

@author: Anna-Lena
"""

import pandas as pd

# Read excel file

mother = pd.read_excel("Muttertabelle.xlsx", sheet_name = 1, header = 2)

# Setze ID_Code(Hexadezimal) als Series Object in Variable
dec = []
seq = mother["ID_Code"]

# Gehe durch Zeilen, rechne Hexadezimal- zu Dezimalzahlen um und schreibe in
# Liste dec

for i in range(0,len(seq)):
    
    hex = str(seq.iloc[i])
    dec.append(int(hex,16))

# Hänge Liste an Dataframe
    
mother.insert(1, 'ID_Dec' ,dec)

data = mother["ID_Dec"]

migrate = pd.read_excel("out.xlsx",sheet_name = 2)

# Leere Liste, in die Indexe wandernder Aale eingetragen werden
where = []

# Check, ob gleiche Werte in Spalte "ID_Dec" in beiden Excel-Files
for i in range(0,len(migrate)):
    val_t0 = int(migrate.iloc[i])
   
    # Stelle des Index der Muttertabelle.xlsx(um 4 korrigiert, da sich die 
    # Indexe von Excel und Pandas unterscheiden und der Header verschoben wurde
    
    find = int(data.loc[data == val_t0].index.values) + 4
    
    where.append(find)
where.sort()
print(where)

## andere Art, um Index zu korrigieren
## correct = [x + 4 for x in where]
## print(correct)

### reverse Dezimal zu Hexadezimal
### schreibe Dezimalzahlen in großbuchstabigen Hexadezimal und slice "0x"

### zuhex = pd.read_excel("Mutter2.xlsx")

### zuhex = zuhex["ID_Dec"].apply(hex).str.upper().str[2:]

### zuhex.to_excel("zuhex.xlsx")
### print(zuhex)