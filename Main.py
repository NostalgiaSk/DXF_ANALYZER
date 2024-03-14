import tkinter as tk
from tkinter import ttk
from Constants.frameConstants import HIGH, WIDTH
from View.homeScreen import start_home_screen




# Create the main window
root = tk.Tk()
root.title("DXF ANALYZER")

# Frame 1 : creation & label
frame1 = tk.Frame(root)
frame1.pack(padx=WIDTH, pady=HIGH)
label1 = tk.Label(frame1, text="DXF ANALYZER", font=("Trebuchet MS", 15, "bold"))
label1.pack(pady=(20, 10)) 



# Create a loading progress bar 
loading_label = tk.Label(frame1, text="Chargement...", font=("Trebuchet MS", 12, "bold"))
loading_label.pack(pady=10)
progress = ttk.Progressbar(frame1, orient="horizontal", length=200, mode="determinate", style="Striped.Horizontal.TProgressbar")
progress.pack(pady=10)  

# Loading logic
def load():
    global i 
    if i <= 10:
        txt = 'Chargement...' + (str(10*i)+'%')
        loading_label.config(text=txt)
        progress['value'] = 10*i
        i += 1
        loading_label.after(400, load)
    else:
        switch_frame()


def switch_frame():
    loading_label.pack_forget()  
    progress.pack_forget()
    frame1.destroy()    
    start_home_screen(frame2)



frame2 = tk.Frame(root)
frame2.pack_forget()
frame2.pack(padx=WIDTH, pady=HIGH)
i = 0
load()

root.resizable(False,False)
root.mainloop()
