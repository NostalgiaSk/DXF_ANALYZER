import tkinter as tk
from tkinter import filedialog
import jinja2
import pdfkit
from datetime import datetime
import sqlite3

#fetch file data from the database
def get_file_data(cursor):
    try:
        cursor.execute("SELECT file_name, perimeter, thickness, speed FROM files")
        file_data = cursor.fetchall()
        return file_data
    except Exception as e:
        print("An error occurred while fetching files:", e)
        return []

# fetch thickness and speed data from the database
def get_thickness_speed_data(cursor):
    try:
        cursor.execute("SELECT thickness, speed FROM thicknesses")
        thickness_speed_data = cursor.fetchall()
        return thickness_speed_data
    except Exception as e:
        print("An error occurred while fetching thickness_speed table data:", e)
        return []


def save_pdf():
    # Get the file path using file dialog
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    
    if output_path:
        try:
           
            conn = sqlite3.connect('files.db')
            cursor = conn.cursor()

            
            file_data = get_file_data(cursor)
            thickness_speed_data = get_thickness_speed_data(cursor)

           
            conn.close()

            
            today_date = datetime.today().strftime("%d %b, %Y")
            month = datetime.today().strftime("%B")

            context = {'file_data': file_data, 'thickness_speed_data': thickness_speed_data, 'today_date': today_date, 'month': month}

            template_loader = jinja2.FileSystemLoader('./')
            template_env = jinja2.Environment(loader=template_loader)

            html_template = 'pdf/report.html'
            template = template_env.get_template(html_template)
            output_text = template.render(context)

            # Configure PDFKit and generate PDF
            config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
            pdfkit.from_string(output_text, output_path, configuration=config, css='pdf/report.css')

        except Exception as e:
            print("An error occurred while generating the report:", e)

