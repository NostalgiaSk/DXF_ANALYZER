

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,ttk


def create_window():
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

    image_image_1 = PhotoImage(file="View/assets/params_assets/image_1.png")
    image_1 = canvas.create_image(
        33.0,
        33.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(file="View/assets/params_assets/button_1.png")
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Discard clicked"),
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
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("Save clicked"),
        relief="flat"
    )
    button_2.place(
        x=551.0,
        y=499.0,
        width=234.0,
        height=39.0
    )


    table = ttk.Treeview(window)
    table['columns'] = ('Name', 'Value')
    table.column('#0', width=0, stretch='no')
    table.column('Name', anchor='w', width=150)
    table.column('Value', anchor='center', width=150)

    table.heading('#0', text='', anchor='w')
    table.heading('Name', text='Parameter Name')
    table.heading('Value', text='Parameter Value')

    table.insert('', 'end', text='1', values=('Parameter 1', 'Value 1'))
    table.insert('', 'end', text='2', values=('Parameter 2', 'Value 2'))

    table.place(x=100, y=100)

    window.resizable(False, False)
    window.mainloop()

# Call the function to create the window
#create_window()
