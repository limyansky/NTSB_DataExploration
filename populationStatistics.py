# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 16:25:26 2022

Exploring large swaths of the NTSB accident database without any particular
goal in mind.

@author: Brent
"""

# Allows database access
import pyodbc

# Plotting and manipulation
import matplotlib.pylab as plt
import numpy as np
import pandas as pd

connect_str = (r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
               r'DBQ=C:\Users\Brent\Documents\Data\NTSB\avall.mdb;')
conn = pyodbc.connect(connect_str)
cursor = conn.cursor()

# =============================================================================
# df = pd.read_sql(('SELECT acft_make, COUNT(acft_make) as num_incidents '
#                   'FROM aircraft '
#                   'GROUP BY acft_make '
#                   'ORDER BY COUNT(acft_make) DESC')
#                  , conn)
# =============================================================================
hour_str = ("SELECT ev_id, Aircraft_Key, flight_hours as {hour_key} "
            "FROM flight_time "
            "WHERE flight_type='{hour_key}' AND flight_craft='ALL' AND flight_hours BETWEEN 40 AND 300;")

L24H = pd.read_sql(hour_str.format(hour_key = 'L24H'), conn)
L30D = pd.read_sql(hour_str.format(hour_key = 'L30D'), conn)
L90D = pd.read_sql(hour_str.format(hour_key = 'L90D'), conn)
TOTL = pd.read_sql(hour_str.format(hour_key = 'TOTL'), conn)

hours = pd.merge(L24H, L30D, on = ['ev_id', 'Aircraft_Key'], how = 'outer')
hours = pd.merge(hours, L90D, on = ['ev_id', 'Aircraft_Key'], how = 'outer')
hours = pd.merge(hours, TOTL, on = ['ev_id', 'Aircraft_Key'], how = 'outer')

hours = hours.sort_values(by=['ev_id'])

plt.clf()
plt.hist(hours['TOTL'], bins=100)
plt.show()