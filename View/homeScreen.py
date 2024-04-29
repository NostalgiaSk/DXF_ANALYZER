from tkinter import Tk, Canvas, Button, PhotoImage, ttk, filedialog, StringVar, Label
import ezdxf
import math
import sqlite3
from tkinter.messagebox import showwarning
from Entities.file import File
from Database.files_database import get_thickness_values, insert_into_files_table, delete_all_files
from View.choose_thickness_screen import create_choose_thickness_window
from View.update_params_screen import create_window

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

    global selected_files_count
    selected_files_count = 0
    def open_file():
        global selected_files_count
        try:
            filepath = filedialog.askopenfilename(filetypes=[("DXF Files", "*.dxf")])
            if filepath:
                if selected_files_count >= 10:
                   showwarning("Limite maximale atteinte", "Vous pouvez selectionner que 10 fichier a la fois .")
                   return
                selected_files_count += 1
                try:
                    doc = ezdxf.readfile(filepath)
                    msp = doc.modelspace()
                    total_perimeter = 0
                    entity_count = 0
                    dashed_line_count = 0
                    file_content = b""
                    min_x = float('inf')
                    max_x = float('-inf')
                    min_y = float('inf')
                    max_y = float('-inf')
                    for entity in msp:
                        perimeter = calculate_perimeter(entity)
                        total_perimeter += perimeter
                        entity_count += 1
                        entity_info = f"Entity Type: {entity.dxftype()}, Perimeter: {perimeter:.2f}\n"
                        file_content += entity_info.encode('utf-8')
                        print(f"Entity {entity_count} Type = {entity.dxftype()}: Perimeter = {perimeter:.2f}")
                        if entity.dxftype() == 'LINE'  and entity.dxf.linetype in ['CENTER', 'CENTER2', 'CENTERX2'] :
                            dashed_line_count += 1
                        # Update min and max coordinates
                        if entity.dxftype() in ['LINE', 'CIRCLE', 'ARC']:
                             min_x, max_x, min_y, max_y = update_min_max_coordinates(entity, min_x, max_x, min_y, max_y)

                    height = max_y - min_y
                    width =  max_x -min_x        
                    print(f"Total perimeter of {entity_count} entities: {total_perimeter:.2f}")
                    print(f"Number of Folds: {dashed_line_count}")
                    print(f"Heigh {height} width {width}")

                    filename = filepath.split("/")[-1]
                    save_file(conn, cursor, filename, total_perimeter, file_content, dashed_line_count,height,width)
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
        command=lambda: reset_table(table, cursor, conn),
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
        command=lambda: save_data_and_navigate_to_result(conn, table, cursor),
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
        command=lambda: navigate_to_update_params(),
        relief="flat"
    )
    button_4.place(
        x=794.0,
        y=17.0,
        width=176.0,
        height=34.0
    )

    def calculate_perimeter(entity):
        # Exclude certain line types
        if hasattr(entity.dxf, 'linetype') and entity.dxf.linetype in ['CENTER', 'CENTER2', 'CENTERX2']:
            return 0

        if entity.dxftype() == 'LINE':
            start_point = entity.dxf.start
            end_point = entity.dxf.end
            return math.hypot(end_point[0] - start_point[0], end_point[1] - start_point[1])
        elif entity.dxftype() == 'CIRCLE':
            radius = entity.dxf.radius
            return 2 * math.pi * radius
        elif entity.dxftype() == 'ARC':
            radius = entity.dxf.radius
            start_angle = math.radians(entity.dxf.start_angle)
            end_angle = math.radians(entity.dxf.end_angle)
            angle = end_angle - start_angle
            if angle < 0:
                angle += 2 * math.pi
            return angle * radius
        elif entity.dxftype() == 'LWPOLYLINE' or entity.dxftype() == 'POLYLINE':
            return calculate_polyline_perimeter(entity)
        elif entity.dxftype() == 'SPLINE':
            return calculate_spline_perimeter(entity)
        else:
            return 0

    def calculate_polyline_perimeter(polyline):
        total_perimeter = 0
        points = polyline.get_points(format='xy')
        for i in range(len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]
            total_perimeter += math.hypot(end_point[0] - start_point[0], end_point[1] - start_point[1])
        if polyline.is_closed:
            total_perimeter += math.hypot(points[-1][0] - points[0][0], points[-1][1] - points[0][1])
        return total_perimeter

    def calculate_spline_perimeter(spline):
        perimeter = 0
        points = spline.control_points
        if len(points) < 2:
            return 0
        for i in range(len(points) - 1):
            x1, y1 = points[i][:2]
            x2, y2 = points[i + 1][:2]
            perimeter += math.hypot(x2 - x1, y2 - y1)
        return perimeter

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
    
    def save_file(conn,cursor ,filename, perimeter, file_content,nb_folds,height,width):
        
        file = File(filename,file_content, perimeter,0,0,0,nb_folds,height,width)
        try:
            insert_into_files_table(file, cursor,conn)
            conn.commit()
        except Exception as e:
            print("An error occurred2:", e)
        conn.commit()
    
    def navigate_to_update_params():
        window.destroy()
        create_window(create_home_window)

    window.resizable(False, False)
    window.mainloop()

def update_min_max_coordinates(entity, min_x, max_x, min_y, max_y):
    if entity.dxftype() == 'CIRCLE':
        center = entity.dxf.center
        if not isinstance(center, tuple):
            center = tuple(center)
        x, y = center[:2]
        radius = entity.dxf.radius
        min_x = min(min_x, x - radius)
        max_x = max(max_x, x + radius)
        min_y = min(min_y, y - radius)
        max_y = max(max_y, y + radius)
    elif entity.dxftype() == 'ARC':
        center = entity.dxf.center
        if not isinstance(center, tuple):
            center = tuple(center)
        x, y = center[:2]
        radius = entity.dxf.radius
        start_angle = math.radians(entity.dxf.start_angle)
        end_angle = math.radians(entity.dxf.end_angle)
        if start_angle > end_angle:
            start_angle, end_angle = end_angle, start_angle  # Ensure start is less than end

        # Calculate bounding box for arc
        angles = [start_angle, end_angle]
        for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:  # Check cardinal points
            if start_angle <= angle <= end_angle:
                angles.append(angle)
        
        for angle in angles:
            test_x = x + radius * math.cos(angle)
            test_y = y + radius * math.sin(angle)
            min_x = min(min_x, test_x)
            max_x = max(max_x, test_x)
            min_y = min(min_y, test_y)
            max_y = max(max_y, test_y)

    elif entity.dxftype() in ['LINE', 'LWPOLYLINE', 'POLYLINE']:
        points = []
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            if not isinstance(start, tuple):
                start = tuple(start)
            if not isinstance(end, tuple):
                end = tuple(end)
            points = [start[:2], end[:2]]
        else:
            points = entity.get_points(format='xy')
        
        for x, y in points:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

    return min_x, max_x, min_y, max_y
