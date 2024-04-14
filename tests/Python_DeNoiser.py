# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 13:07:39 2023

@author: Erik Lehmann
"""
import pandas as pd

### Hier kannst du Variablen eingeben

# Die Zeiten, die als Aalsignal akzeptiert werden
time_tolerance = [5,6,7,11,12,13,17,18,19]

# Die Zeitdistanz von Messpunkt i zu Messpunkt i+2, die toleriert wird
distance_tolerance = 60

# Die Spaltennamen, die du gern für deine Exceltabelle benutzen möchtest(mit Komma zu trennen)
# Bitte unbedingt die Spalten "Receiver", "DATE", "SECOND_DAY" und "ID_HEX" behalten oder 
# im gesamten Programm abändern

usedcolumns = ['Nr','Receiver','Date_Time','FracSec','ID_Dec','ID_HEX','Power','Standort','DATE','TIME','SECOND_DAY']
#-----------------------------------------------------------------------------
fileinput = input("Bitte gib mir den Pfad deiner Excel(xlsx) - Datei in dem Format C:\Verzeichnis\Verzeichnis\...\Datei ") + ".xlsx"
tabelleninput = input("Wie ist der exakte Name(Groß- und Kleinschreibung beachten) des Tabellenblattes, das bearbeitet werden soll? ")
df = pd.read_excel(fileinput,sheet_name = tabelleninput, usecols = usedcolumns).drop_duplicates(subset =['Receiver','DATE','SECOND_DAY']).reset_index(drop=True)


### zum Test
# df.to_pickle("dataframe.pk1")
# df = pd.read_pickle("dataframe.pk1")

# Liste von Signalen ob Aal ja oder nein
# Beim ersten Signal können wir nichts feststellen, da es keine Differenz gibt
is_eel = []


# Wir müssen uns den Index des letzten Aal abspeichern
# wenn wir ggf. mehrere Aale überspringen
last_eel = 0
# Das Gleiche gilt für das Datum und die ID, da diese ebenfalls abgeglichen werden
comp_var = 2

#Außerdem brauche ich den dritten Aal in einer Reihe für den Test bei distance3
# third_eel = 2
# Pandas Series object in Variable schreiben
seq = pd.Series(df['SECOND_DAY']).round(decimals=0)

# Datum in Variable schreiben
date = df['DATE']

#ID in Variable schreiben
eel_id = df['ID_HEX']

# Mit range(1, len(seq)) erzeuge ich eine ganzzahl list von 1 bis zur 
# maximalen größe von seq
for i in range(1,len(seq)):
    
    if comp_var == len(seq):
        break
    # Ich hole mir den Wert T0 und T-1
    # Und schaue mir die Distanz an
    val_last_eel = seq.iloc[last_eel]
    val_eel = seq.iloc[i]
    val_third_eel = seq.iloc[comp_var]
    # test_id = eel_id.iloc[comp_id]
    
    distance = round(abs(val_eel - val_last_eel))
    
    # Die Distanz zwischen 3 Messungen
    distance3 = round(abs(val_third_eel - val_last_eel))
    
    
    # wenn zwischen zwei Daten ein 6-er Intervall, drei aufeinanderfolgenden 
    # Messungen im Bereich von 60 sek liegen, das Datum dieser drei Messungen
    # und die ID der 3 betrachteten Hydrophone übereinstimmen
     
    if date.iloc[i-1] == date.iloc[comp_var] and date.iloc[i] == date.iloc[comp_var] and eel_id.iloc[i-1] == eel_id.iloc[comp_var] and eel_id.iloc[i] == eel_id.iloc[comp_var] and distance >= 5 and distance in time_tolerance and distance3 <= distance_tolerance:
        # ist ein Aal-Signal
        is_eel.append(1)
    else:
        # Sonst falsch
        is_eel.append(0)
    last_eel = i
    comp_var = i+2
    # third_eel = i+2
    # print(i, val_t0, val_t1, val_t0 - val_t1)

# df['distance'] = distance
# s3 = [0,0]
# is_eel = pd.concat([is_eel,s3], ignore_index = True)
df.insert(len(df.columns), 'is_eel' ,is_eel+['n/a','n/a'], allow_duplicates = True)

# df.to_csv('out.csv',index = False)
df.to_excel('out.xlsx',index = False)
