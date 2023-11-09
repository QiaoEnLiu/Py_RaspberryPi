# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:25:36 2023

@author: User
"""
import sqlite3

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# 建立表
cursor.execute('''CREATE TABLE IF NOT EXISTS mytable
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT)''')

conn.commit()
conn.close()