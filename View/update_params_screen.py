from tkinter import Tk, Canvas, Button, Entry, PhotoImage
import sqlite3

def fetch_data_from_database():
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM thicknesses''')
    data = cursor.fetchall()
    conn.close()
    return data

def create_window(create_home_func):
    window = Tk()
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

    # Fetch data from the database
    data = fetch_data_from_database()

    # Create Entry widgets to display and edit the data
    entries = []
    for row in data:
        entry_id = row[0]  # Assuming the first column is the unique identifier
        for value in row[1:]:
            entry = Entry(window)
            entry.insert(0, str(value))
            entry.grid(row=entry_id, column=len(entries) + 1)
            entries.append((entry_id, entry))

    button_image_1 = PhotoImage(file="View/assets/params_assets/button_1.png")
    button_1 = Button(
        window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: return_to_home(window, create_home_func),
        relief="flat"
    )
    button_1.place(
        x=219.0,
        y=499.0,
        width=234.0,
        height=39.0
    )

    button_image_2 = PhotoImage(file="View/assets/params_assets/button_2.png")
    button_2 = Button(
        window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: save_changes(entries),
        relief="flat"
    )
    button_2.place(
        x=551.0,
        y=499.0,
        width=234.0,
        height=39.0
    )

    window.resizable(False, False)
    window.mainloop()

def save_changes(entries):
    conn = sqlite3.connect('files.db')
    cursor = conn.cursor()
    for entry_id, entry_widget in entries:
        value = entry_widget.get()
        cursor.execute('''UPDATE thicknesses SET thickness = ? WHERE id = ?''', (value, entry_id))
    conn.commit()
    conn.close()




def return_to_home(window, create_home_func):
    window.destroy()
    create_home_func()

