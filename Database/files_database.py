import sqlite3
from Entities.file import File
from Entities.thickness import Thickness

conn = sqlite3.connect('files.db')
cursor = conn.cursor()


def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS files
                      (id INTEGER PRIMARY KEY ,
                       file_name TEXT,
                       dxf_blob BLOB,
                       perimeter REAL,
                       thickness REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS thicknesses
                      (id INTEGER PRIMARY KEY ,
                       thickness REAL)''')
    
                   
# for value in range(1, 6):
#     cursor.execute("INSERT INTO thicknesses (thickness) VALUES (?)", (value,))

def update_thickness_in_database(cursor, new_thickness):
    try:
        cursor.execute("UPDATE files SET thickness = ?", (new_thickness,))
        conn.commit()
        print("Thickness updated successfully.")
    except sqlite3.Error as e:
        print("An error occurred while updating thickness:", e)

conn.commit()

#Insert values to table after selection

def insert_into_files_table(file: File, cursor,conn):
    try:
        cursor.execute("INSERT INTO files (file_name, dxf_blob, perimeter, thickness) VALUES (?, ?, ?, ?)",
                       (file.file_name, sqlite3.Binary(file.file_content), file.perimeter, file.thickness))
        conn.commit()
        print("File saved successfully.")
    except Exception as e:
        print("An error occurred 3:", e)

def delete_all_files(cursor):
    try:
        cursor.execute("DELETE FROM files")
        conn.commit()
        print("All content deleted from the 'files' table.")
    except Exception as e:
        print("An error occurred 4:", e)

def get_thickness_values(cursor):
    cursor.execute("SELECT thickness FROM thicknesses")
    thickness_values = cursor.fetchall()
    return thickness_values

def init_databases(conn,cursor):
    cursor.execute("DELETE FROM files")
    cursor.execute("DELETE FROM thicknesses")
    for value in range(1, 6):
       cursor.execute("INSERT INTO thicknesses (thickness) VALUES (?)", (value,))
    conn.commit()

conn.close()