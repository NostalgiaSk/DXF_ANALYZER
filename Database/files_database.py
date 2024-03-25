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
                       thickness REAL,
                       speed REAL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS thicknesses
                      (id INTEGER PRIMARY KEY ,
                       thickness REAL UNIQUE,
                       speed REAL UNIQUE)''')



def init_databases(conn, cursor):
    try:
        cursor.execute("DELETE FROM files")
        cursor.execute("DELETE FROM thicknesses")
        
        thickness_speed_values = [
            (1, 10),  
            (2, 20),  
            (3, 30),  
            (4, 40),  
            (5, 50) 
        ]
        
        for thickness, speed in thickness_speed_values:
            print(thickness, speed)
            cursor.execute("INSERT INTO thicknesses (thickness, speed) VALUES (?, ?)", (thickness, speed))
        
        conn.commit()
        print("Initialization successful.")
    except Exception as e:
        print("An error occurred during initialization:", e)
        conn.rollback()  # Rollback changes if an error occurs

    
      


#FILES TABLE MANIPULATION
def update_thickness_in_database(cursor, new_thickness,new_speed,conn):
    try:
        cursor.execute("UPDATE files SET thickness = ?", (new_thickness,))
        cursor.execute("UPDATE files SET speed = ?", (new_speed,))
        conn.commit()
        print("Thickness and speed updated successfully.")
    except sqlite3.Error as e:
        print("An error occurred while updating thickness:", e)

conn.commit()


def insert_into_files_table(file: File, cursor, conn):
    try:
        cursor.execute("INSERT INTO files (file_name, dxf_blob, perimeter, thickness, speed) VALUES (?, ?, ?, ?, ?)",
                       (file.file_name, sqlite3.Binary(file.file_content), file.perimeter, file.thickness, file.cutting_speed))
        conn.commit()
        print("File saved successfully.")
    except Exception as e:
        print("An error occurred 3:", e)


def delete_all_files(cursor,conn):
    try:
        cursor.execute("DELETE FROM files")
        conn.commit()
        print("All content deleted from the 'files' table.")
    except Exception as e:
        print("An error occurred 4:", e)


def get_file_data(conn,cursor):
    try:
        cursor.execute("SELECT file_name, perimeter, thickness,speed FROM files")
        file_data = cursor.fetchall() 
        conn.close()  
        return file_data
    except Exception as e:
        print("An error occurred while fetching files:", e)
        return []


#THICKNESS TABLE MANIPULATION
def get_thickness_values(cursor):
    cursor.execute("SELECT thickness FROM thicknesses")
    thickness_values = cursor.fetchall()
    return thickness_values



def fetch_cuuting_speed(cursor, thickness):
    try:
        cursor.execute("SELECT speed FROM thicknesses WHERE thickness = ?", (thickness,))
        speed_result = cursor.fetchone()
        if speed_result:
            return speed_result[0]
        else:
            print(f"No speed found for thickness {thickness}.")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None
    



conn.close()