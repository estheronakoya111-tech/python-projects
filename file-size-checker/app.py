import tkinter as tk
from tkinter import filedialog
import os


# Create the main application window
root = tk.Tk()
root.title("File Size Checker")
root.geometry("400x300")


# Create the main frame
frame = tk.Frame(root, bg="#f5f7fa")
frame.pack()


# Function to choose a file and display its information
def choose_file():
    file_path = filedialog.askopenfilename()

    # Check if a file was actually selected
    if file_path:

        # Get the file size in bytes
        file_size = os.path.getsize(file_path)

        # Convert the file size to MB if it is 1 MB or larger
        if file_size >= 1024 * 1024:
            file_size_mb = file_size / (1024 * 1024)
            display_size = f"{file_size_mb:.2f} MB"

        # Otherwise, convert the file size to KB
        else:
            file_size_kb = file_size / 1024
            display_size = f"{file_size_kb:.2f} KB"

        # Get the file name from the full file path
        file_name = os.path.basename(file_path)

        # Get the file extension and remove the dot
        file_type = os.path.splitext(file_name)[1].upper().lstrip(".")

        # Display the file information
        result_label.config(
            text=f"File: {file_name}\nType: {file_type}\nSize: {display_size}"
        )


# Function to clear the displayed file information
def clear_result():
    result_label.config(text="")


# Create the title
title_label = tk.Label(
    frame,
    text="File Size Checker",
    font=("Arial", 20, "bold"),
    bg="#f5f7fa"
)
title_label.pack()


# Create the Choose File button
button = tk.Button(
    frame,
    text="Choose File",
    command=choose_file,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8,
    bg="#2563eb",
    fg="white"
)
button.pack()


# Create the Clear button
clear_button = tk.Button(
    frame,
    text="Clear",
    command=clear_result,
    font=("Arial", 11),
    padx=15,
    pady=6
)
clear_button.pack(pady=5)


# Create the label that displays the file information
result_label = tk.Label(
    frame,
    text="",
    font=("Arial", 12),
    pady=10,
    bg="#f5f7fa"
)
result_label.pack(pady=15)


# Keep the application running
root.mainloop()