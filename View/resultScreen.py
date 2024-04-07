from tkinter import Tk, Canvas, Button, PhotoImage, ttk, filedialog , StringVar , Label
import ezdxf  
import math
from Database.files_database import get_file_data , update_file_cutting_time
import sqlite3
from pdf.pdf_generation import save_pdf


def create_result_window():
    window = Tk()
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()

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

    text_label = Label(window, text="Resultat", bg="#FFFFFF", font=("Arial", 14, "bold"), fg="#030088")
    text_label.place(x=470, y=120)

    # Add the table
    table = ttk.Treeview(window)
    table["columns"] = ("Fichier", "Perimetre","Epaisseur", "Vitesse","Temps Decoupage")
    table.column("#0", width=0, stretch=False)
    table.column("Fichier", anchor="w", width=300)
    table.column("Perimetre", anchor="center", width=200)
    table.column("Epaisseur", anchor="center", width=100)
    table.column("Vitesse", anchor="center", width=100)
    table.column("Temps Decoupage", anchor="center", width=200)
    table.heading("#0", text="", anchor="w")
    table.heading("Fichier", text="Filename", anchor="center")
    table.heading("Perimetre", text="Perimeter", anchor="center")
    table.heading("Epaisseur", text="Epaisseur", anchor="center")
    table.heading("Vitesse", text="Vitesse", anchor="center")
    table.heading("Temps Decoupage", text="Temps Decoupage", anchor="center")
    table.place(x=50, y=200)

    image_image_1 = PhotoImage(file="View/assets/home_assets/image_1.png")
    image_1 = canvas.create_image(
        33.0,
        33.0,
        image=image_image_1
    )


    button_image_3 = PhotoImage(file="View/assets/result_assets/button_1.png")
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: save_pdf(),
        relief="flat"
    )
    button_3.place(
        x=370.0,
        y=500.0,
        width=274,
        height=40.0
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




    def fill_table(conn,cursor,table):
        try:
            file_data=get_file_data(conn,cursor)
            for file_entry in file_data:
                 filename, perimeter, thickness,speed = file_entry
                 duration = perimeter/speed
                 update_file_cutting_time(conn,cursor,filename,duration)
                 table.insert("", "end", values=(filename, perimeter, thickness, speed,duration))

        except Exception as e:
            print("An error occurred while fetching files:", e)


    window.resizable(False, False)
    fill_table(conn,cursor,table)
    window.mainloop()






#create_result_window()