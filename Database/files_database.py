import sqlite3
from Model.file import File
conn = sqlite3.connect('files.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS files
                  (id INTEGER PRIMARY KEY ,
                   file_name TEXT,
                   perimeter REAL,
                   thickness REAL)''')

conn.commit()

#Insert values to table after selection

def insert_into_files_table(file : File):
    with conn :
        c.execute("INSERT INTO files VALUES  (:name, :perimeter)" , {'name' : file.file_name , 'perimeter' :file.perimeter})


conn.close()