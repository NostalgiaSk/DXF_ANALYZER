import sqlite3
from Entities.file import File
from Entities.thickness import Thickness

conn = sqlite3.connect('files.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS files
                  (id INTEGER PRIMARY KEY ,
                   file_name TEXT,
                   perimeter REAL,
                   thickness REAL)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS thicknesses
                  (id INTEGER PRIMARY KEY ,
                   thickness REAL)''')

conn.commit()

#Insert values to table after selection

def insert_into_files_table(file : File):
    with conn :
        c.execute("INSERT INTO files VALUES  (:name, :perimeter)" , {'name' : file.file_name , 'perimeter' :file.perimeter})
        

def get_thickness_values():
    cursor.execute("SELECT thickness FROM thicknesses")
    thickness_values = cursor.fetchall()
    return [thickness[0] for thickness in thickness_values]


conn.close()