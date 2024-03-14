import tkinter as tk
from tkinter import filedialog
import ezdxf
import math
from scipy.interpolate import BSpline  



def start_home_screen(frame):
    label = tk.Label(frame, text="Acceuil", font=("Trebuchet MS", 15, "bold"))
    label.pack(pady=20)
    button = tk.Button(frame, text="Ouvrir un fichier", command=open_file, font=("Trebuchet MS", 12))
    button.pack(pady=20)


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
        # Check if the entity has a 'fit_points' attribute, which is used for Bezier splines
        if hasattr(entity, 'fit_points'):
            control_points = entity.fit_points
        else:
            # Otherwise, assume it's a B-spline and access control points directly
            control_points = entity.control_points()
        
        # Calculate perimeter by summing distances between consecutive control points
        for i in range(len(control_points) - 1):
            ds = math.sqrt((control_points[i][0] - control_points[i + 1][0]) ** 2 + 
                           (control_points[i][1] - control_points[i + 1][1]) ** 2)  
            total_perimeter += ds
        return total_perimeter
    else:
        return 0



def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("DXF Files", "*.dxf")])
    if filepath:
        doc = ezdxf.readfile(filepath)
        msp = doc.modelspace()
        total_perimeter = 0
        entity_count = 0
        for entity in msp:
            perimeter = calculate_perimeter(entity)
            total_perimeter += perimeter
            entity_count += 1
            print(f"Entity {entity_count}: Perimeter = {perimeter:.2f}")
        print(f"Total perimeter of {entity_count} entities: {total_perimeter:.2f}")



