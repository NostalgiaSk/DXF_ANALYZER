from tkinter import Tk, Canvas, Button, PhotoImage, ttk, filedialog , StringVar , Label
import ezdxf  
import math
from Database.files_database import get_file_data,get_thickness_values, update_file_data , fetch_cutting_speed
import sqlite3
from tkinter.messagebox import showwarning
from View.resultScreen import create_result_window



def create_choose_thickness_window():
    window = Tk()
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()

    thickness_values = get_thickness_values(cursor)

    window.geometry("1000x600")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=600,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_rectangle(
        0.0,
        0.0,
        1000.0,
        66.0,
        fill="#020088",
        outline=""
    )

    canvas.create_text(
        61.0,
        19.0,
        anchor="nw",
        text="DXF ANALYZER",
        fill="#FFFFFF",
        font=("Lemonada Bold", 16 * -1)
    )

    text_label = Label(window, text="Choisir un epaisseur pour chaque fichier ", bg="#FFFFFF", font=("Arial", 14, "bold"), fg="#030088")
    text_label.place(x=320, y=120)


    image_image_1 = PhotoImage(file="View/assets/home_assets/image_1.png")
    image_1 = canvas.create_image(
        33.0,
        33.0,
        image=image_image_1
    )


    button_image_3 = PhotoImage(file="View/assets/home_assets/button_3.png")
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:save_data_and_navigate_to_result(conn, cursor),
        relief="flat"
    )

    button_3.place(
        x=420.0,
        y=500.0,
        width=170,
        height=34.0
    )

    button_image_4 = PhotoImage(file="View/assets/home_assets/button_4.png")
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    button_4.place(
        x=794.0,
        y=17.0,
        width=176.0,
        height=34.0
    )



    def display_file_comboboxes(conn,cursor):
        try:
            file_data = get_file_data(conn, cursor)
            row = 200  # Starting y-coordinate for positioning labels and comboboxes
            for file_entry in file_data:
                 filename, _, _, _ = file_entry
                 display_filename = filename[:20] + "..." if len(filename) > 20 else filename
                 label = Label(window, text=display_filename, bg="#FFFFFF", font=("Arial", 12), anchor="w", width=20)
                 label.place(x=320, y=row)
                 combobox = ttk.Combobox(window, values=thickness_values, state="readonly")
                 combobox.place(x=550, y=row)
                 combobox.bind("<<ComboboxSelected>>", lambda event, f=filename, c=combobox: on_combobox_select(event, f, c))
                 row += 30  # Increase y-coordinate for next file

        except :
            print("An error occurred while fetching file  Names:", e)
    

    def on_combobox_select(event, filename, combobox):
       conn = sqlite3.connect('files.db')
       cursor = conn.cursor()
       thickness = combobox.get()
       speed = fetch_cutting_speed(conn,cursor, thickness)
       if speed is not None:
         update_file_data(conn, cursor, filename, thickness, speed)
       else:
          # Handle case where speed is not found for the selected thickness
          showwarning("Error", f"No speed found for thickness {thickness}.")


    def save_data_and_navigate_to_result(conn,cursor):
        conn.commit()
        window.destroy()
        create_result_window() 


    

    display_file_comboboxes(conn,cursor)
    window.resizable(False, False)
    window.mainloop()






#create_choose_thickness_window()