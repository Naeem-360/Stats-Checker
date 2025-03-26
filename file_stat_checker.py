import os
import time
import tkinter as tk
from tkinter import filedialog, scrolledtext
import random

# File info checker function
def file_info_checker(file_path):
    try:
        file_info = os.stat(file_path)
        return (
            f"Last Modified: {time.ctime(file_info.st_mtime)}\n"
            f"Last Accessed: {time.ctime(file_info.st_atime)}\n"
            f"Last Changed: {time.ctime(file_info.st_ctime)}\n"
            f"Mode: {oct(file_info.st_mode)}\n"
            f"Group ID: {file_info.st_gid} (Usually meaningless on Windows)"
        )
    except Exception as e:
        return f"Error: {e}"

# Open file dialog and update text box
def open_file_dialog():
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
    )
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)

# Check file info and display it
def check_file_info():
    file_path = path_entry.get()
    if file_path:
        result = file_info_checker(file_path)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Please enter or select a file path!")

# Snow animation function
def animate_snow():
    canvas.delete("snow")  # Clear previous snowflakes
    for flake in snowflakes:
        flake[1] += flake[2]  # Move y-position down by speed
        if flake[1] > 400:  # Reset to top if off-screen
            flake[1] = random.randint(-20, 0)
            flake[0] = random.randint(0, 500)
        canvas.create_oval(flake[0], flake[1], flake[0] + 5, flake[1] + 5, fill="white", tags="snow")
    root.after(50, animate_snow)

# Close the window
def close_window():
    root.quit()

# Drag functionality
def start_drag(event):
    root.x = event.x  # Store initial x position
    root.y = event.y  # Store initial y position

def drag_window(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

# Set up the GUI window
root = tk.Tk()
root.title("File Info Checker")
root.geometry("500x400")
root.attributes("-alpha", 0.9)  # Slightly transparent
root.overrideredirect(True)  # Remove default window borders, no resizing

# Canvas for window and snow
canvas = tk.Canvas(root, width=500, height=400, highlightthickness=0, bg="black")
canvas.pack(fill="both", expand=True)

# Draw rounded GUI border (using an oval for simplicity)
canvas.create_oval(10, 10, 490, 390, fill="#1a1a1a", outline="", tags="silver_gui")  # Silver-gray inner area

# Snowflakes: [x, y, speed]
snowflakes = [[random.randint(0, 500), random.randint(-50, 400), random.uniform(1, 3)] for _ in range(30)]
animate_snow()  # Start snow animation

# Bind drag events to black edges and silver GUI
canvas.bind("<Button-1>", start_drag)  # Click on black background
canvas.bind("<B1-Motion>", drag_window)  # Drag on black background
canvas.tag_bind("silver_gui", "<Button-1>", start_drag)  # Click on silver area
canvas.tag_bind("silver_gui", "<B1-Motion>", drag_window)  # Drag on silver area

# Frame for widgets (centered in the rounded area)
frame = tk.Frame(canvas, bg="#1a1a1a")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Label and text box
tk.Label(frame, text="File Path:", fg="silver", font=("Arial", 12), bg="#1a1a1a").pack(pady=5)
path_entry = tk.Entry(frame, width=40, bg="#333333", fg="silver", insertbackground="silver", borderwidth=2)
path_entry.pack(pady=5)

# Scrolled text area for output
output_text = scrolledtext.ScrolledText(frame, width=40, height=10, bg="#333333", fg="silver", font=("Arial", 10), borderwidth=2)
output_text.pack(pady=10)

# Buttons with "rounded" look (using canvas ovals behind buttons)
button_frame = tk.Frame(frame, bg="#1a1a1a")
button_frame.pack(pady=5)

# Open button with rounded background
open_button_bg = canvas.create_oval(180, 300, 260, 340, fill="silver", outline="", tags="button_bg")
open_button = tk.Button(button_frame, text="Browse File", command=open_file_dialog, bg="silver", fg="black", font=("Arial", 10), relief="flat", bd=0, padx=10, pady=5)
open_button.pack(side="left", padx=5)

# Check button with rounded background
check_button_bg = canvas.create_oval(280, 300, 360, 340, fill="silver", outline="", tags="button_bg")
check_button = tk.Button(button_frame, text="Check Info", command=check_file_info, bg="silver", fg="black", font=("Arial", 10), relief="flat", bd=0, padx=10, pady=5)
check_button.pack(side="left", padx=5)

# Close button (top-right corner, rounded)
close_button_bg = canvas.create_oval(450, 20, 470, 40, fill="red", outline="")
close_button = tk.Button(canvas, text="X", command=close_window, bg="red", fg="white", font=("Arial", 10), relief="flat", bd=0, width=1, height=1)
close_button.place(x=455, y=25)

# Start the GUI
if __name__ == "__main__":
    root.mainloop()