# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 18:45:58 2023

@author: TheRickestRick
"""

import pandas as pd



wander = pd.read_excel('out.xlsx', usecols=['Ort','DATUM','ID_HEX','Receiver','is_eel'], dtype = {'Nr':str})
# wander.dropna(axis = 0, subset=['is_eel'], inplace=True)
wanderpivot = pd.pivot_table(wander, values='is_eel', index=['Ort', 'ID_HEX','DATUM'], columns='Receiver')
with pd.ExcelWriter('out2.xlsx') as writer:
    for i, x in wanderpivot.groupby('ID_HEX'):
        x.to_excel(writer, sheet_name=i, index=True)
# wanderdate = wander.query("is_eel>0")
# unid = list(set(wanderdate['ID_HEX']))
# wanderdate = wanderdate['ID_HEX']
# unid = pd.unique(wanderdate['ID_HEX'])

datelist_min = []
datelist_max = []

    
#     datelist_min.append(spec['DATUM'].min())
#     datelist_max.append(spec['DATUM'].max())