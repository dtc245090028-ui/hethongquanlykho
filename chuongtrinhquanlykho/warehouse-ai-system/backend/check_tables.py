#!/usr/bin/env python
import sqlite3

db_path = 'warehouse.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('Tables in database:')
if not tables:
    print('  (no tables)')
else:
    for table in tables:
        print(f'  - {table[0]}')
    
conn.close()
