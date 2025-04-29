import sqlite3

conn = sqlite3.connect('angel_store.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM books")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()