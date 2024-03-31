from tkinter import Tk, Canvas, Button, PhotoImage, ttk, filedialog , StringVar , Label
import ezdxf  
import math
from Database.files_database import get_thickness_values , insert_into_files_table,delete_all_files
import sqlite3
from tkinter.messagebox import showwarning
from Entities.file import File
from View.choose_thickness_screen import create_choose_thickness_window



def create_home_window():
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

    # Add the table
    table = ttk.Treeview(window)
    table["columns"] = ("Filename", "Perimeter")
    table.column("#0", width=0, stretch=False)
    table.column("Filename", anchor="w", width=300)
    table.column("Perimeter", anchor="center", width=200)
    table.heading("#0", text="", anchor="w")
    table.heading("Filename", text="Filename", anchor="w")
    table.heading("Perimeter", text="Perimeter", anchor="center")
    table.place(x=250, y=200)

    image_image_1 = PhotoImage(file="View/assets/home_assets/image_1.png")
    image_1 = canvas.create_image(
        33.0,
        33.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(file="View/assets/home_assets/button_1.png")

    def open_file():
        try:
            filepath = filedialog.askopenfilename(filetypes=[("DXF Files", "*.dxf")])
            if filepath:
                try:
                    doc = ezdxf.readfile(filepath)
                    msp = doc.modelspace()
                    total_perimeter = 0
                    entity_count = 0
                    file_content = b""
                    for entity in msp:
                        perimeter = calculate_perimeter(entity)
                        total_perimeter += perimeter
                        entity_count += 1
                        entity_info = f"Entity Type: {entity.dxftype()}, Perimeter: {perimeter:.2f}\n"
                        file_content += entity_info.encode('utf-8')
                        print(f"Entity {entity_count} Type = {entity.dxftype()}: Perimeter = {perimeter:.2f}")
                    print(f"Total perimeter of {entity_count} entities: {total_perimeter:.2f}")
                    filename = filepath.split("/")[-1]
                    save_file(conn,cursor, filename, total_perimeter, file_content)
                    table.insert("", "end", values=(filename, f"{total_perimeter:.2f}")) 
                except IOError:
                    print("Not a DXF file or a generic I/O error.")
                except ezdxf.DXFStructureError:
                    print("Invalid or corrupted DXF file.")
        except Exception as e:
            print("An error occurred 1:", e)

    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=open_file,
        relief="flat"
    )
    button_1.place(
        x=408.0,
        y=117.0,
        width=207.0,
        height=36.02940368652344
    )

    button_image_2 = PhotoImage(file="View/assets/home_assets/button_2.png")
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: reset_table(table,cursor,conn),
        relief="flat"
    )
    button_2.place(
        x=324.0,
        y=527.0,
        width=170.0,
        height=34.0
    )

    button_image_3 = PhotoImage(file="View/assets/home_assets/button_3.png")
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:save_data_and_navigate_to_result(conn,table, cursor),
        relief="flat"
    )
    button_3.place(
        x=534.0,
        y=527.0,
        width=170.0,
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

    def calculate_perimeter(entity):
        if entity.dxftype() == 'LINE':
            start_point = entity.dxf.start
            end_point = entity.dxf.end
            return start_point.distance(end_point)
        elif entity.dxftype() == 'CIRCLE':
            radius = entity.dxf.radius
            return 2 * math.pi * radius
        elif entity.dxftype() == 'ARC':
            radius = entity.dxf.radius
            angle = entity.dxf.end_angle - entity.dxf.start_angle
            return (angle / 360) * 2 * math.pi * radius
        elif entity.dxftype() == 'LWPOLYLINE' or entity.dxftype() == 'POLYLINE':
            total_perimeter = 0
            for segment in entity.get_points():
                start_point = segment[0]
                end_point = segment[-1]
                total_perimeter += start_point.distance(end_point)
            return total_perimeter
        elif entity.dxftype() == 'SPLINE':
            total_perimeter = 0
            if hasattr(entity, 'fit_points'):
                control_points = entity.fit_points
            elif hasattr(entity, 'control_points'):
                control_points = entity.control_points()
            else:
                control_points = list(entity.approximate_fit_points())

            for i in range(len(control_points) - 1):
                ds = math.sqrt((control_points[i][0] - control_points[i + 1][0]) ** 2 + 
                            (control_points[i][1] - control_points[i + 1][1]) ** 2)  
                total_perimeter += ds
            return total_perimeter
        else:
            return 0

    def reset_table(table ,cursor,conn):
        table.delete(*table.get_children()) 
        delete_all_files(cursor,conn)
        

    def save_data_and_navigate_to_result(conn,table,cursor):
        if not table.get_children():
            showwarning("Empty Table", "The table is empty!")
            return
        conn.commit()
        window.destroy()
        create_choose_thickness_window()
    
    def save_file(conn,cursor ,filename, perimeter, file_content):
        
        file = File(filename,file_content, perimeter,0,0)
        try:
            insert_into_files_table(file, cursor,conn)
            conn.commit()
        except Exception as e:
            print("An error occurred2:", e)
        conn.commit()

    window.resizable(False, False)
    window.mainloop()





