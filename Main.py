from tkinter import Tk, Canvas, PhotoImage
from tkinter.ttk import Progressbar, Style
from pathlib import Path
from View.homeScreen import create_home_window
import sqlite3
from Database.files_database import create_tables ,init_databases


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / path

window = Tk()
window.geometry("850x450")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=450,
    width=850,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

canvas.create_rectangle(
    0.0,
    0.0,
    850.0,
    162.0,
    fill="#020088",
    outline=""
)

# Create "DXF ANALYZER" text
canvas.create_text(
    324.0,
    102.0,
    anchor="nw",
    text="DXF ANALYZER",
    fill="#FFFFFF",
    font=("Lemonada Bold", 24, "bold")
)

# Load and display the image
image_img1 = PhotoImage(file="images/dxf.png")
resized_img1 = image_img1.subsample(6, 6)  # adjust subsampling factor as needed
text_coords = canvas.bbox(canvas.find_all()[1])  # Assuming it's the second item on the canvas
img_x = (text_coords[0] + text_coords[2]) / 2  # Centering horizontally
img_y = text_coords[1] - 50  # 50 pixels above the text
img1 = canvas.create_image(
    img_x,
    img_y,
    anchor="center",
    image=resized_img1
)

# Create loading label
loading_label = canvas.create_text(
    372.0,
    240.0,
    anchor="nw",
    text="Chargement...",
    fill="#020088",
    font=("Trebuchet MS", 12, "bold")
)

# Custom progress bar style
style = Style()
style.theme_use("default")
style.configure("Custom.Horizontal.TProgressbar", foreground="#FFFFFF", background="#030088")

# Create progress bar
progress = Progressbar(
    window,
    orient="horizontal",
    length=220,
    mode="determinate",
    style="Custom.Horizontal.TProgressbar"
)
progress.place(x=325, y=295)

# Loading logic
i = 0
def load():
    global i
    if i <= 10:
        txt = 'Chargement...' + (str(10*i)+'%')
        canvas.itemconfigure(loading_label, text=txt)
        progress['value'] = 10*i
        i += 1
        window.after(200, load)
    else:
        switch_frame()

def switch_frame():
    canvas.delete(loading_label)
    window.destroy()
    create_home_window()   
   

# Start the loading
load()
#init database tables
conn = sqlite3.connect('files.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS  thicknesses")
cursor.execute("DROP TABLE IF EXISTS  files")
create_tables(cursor)
init_databases(conn,cursor)




window.mainloop()
