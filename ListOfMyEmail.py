import tkinter as tk
import customtkinter
from tkinter import scrolledtext
w = customtkinter.CTk(fg_color='grey')
w.geometry("600x440")
w.title('LisofMyEmail')
SendMailframe = customtkinter.CTkFrame(master=w, width=320, height=400, corner_radius=15,fg_color='white')
SendMailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
Welcome = customtkinter.CTkLabel(master=SendMailframe, text="My Email", font=('Century Gothic', 20))
Welcome.place(relx=0.5, y=40,anchor=tk.CENTER)
# it just a testor for table
emails = [
    "Sender: john@example.com",
    "Subject: Meeting Reminder",
    "Date: 2023-01-15",
        "Sender: john@example.com",
    "Subject: Meeting Reminder",
    "Date: 2023-01-15",
        "Sender: john@example.com",
    "Subject: Meeting Reminder",
    "Date: 2023-01-15",
        "Sender: john@example.com",
    "Subject: Meeting Reminder",
    "Date: 2023-01-15",
        "Sender: john@example.com",
    "Subject: Meeting Reminder",
    "Date: 2023-01-15",
        "Sender: john@example.com",
  
]
# Create a canvas and scrollbar to contain the table
canvas = tk.Canvas(SendMailframe, bg='white', width=300, height=240)
canvas.place(relx=0.5, anchor=tk.CENTER, y=200)
scrollbar = customtkinter.CTkScrollbar(SendMailframe, orientation="vertical", command=canvas.yview, height=240)
scrollbar.place(relx=0.95, anchor=tk.CENTER, y=200)
# Create a frame inside the canvas to hold the table
table_frame = customtkinter.CTkFrame(master=canvas, fg_color='white')
# Attach the frame to the canvas
canvas.create_window((0, 0), window=table_frame, anchor='nw')
# Create the table inside the frame
for i, value in enumerate(emails):
    # Create a frame for each row
    row_frame = customtkinter.CTkFrame(master=table_frame)
    row_frame.grid(row=i, column=0, sticky="ew")
    # Add label with text
    cell = customtkinter.CTkLabel(master=row_frame, text=value, corner_radius=6, fg_color='white')
    cell.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    # Add separator line
    separator = tk.Frame(master=row_frame, height=1,width=285, bg="grey")
    separator.grid(row=1, column=0, sticky="ew")
# Configure the canvas scroll region
table_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)
# Set column width
table_frame.grid_columnconfigure(0, weight=1)
# Adjust grid weights to make the table expand properly
for i in range(len(emails)):
    table_frame.grid_rowconfigure(i, weight=1)
back = tk.Button(master=SendMailframe, width=10, height=1, text="Back", font=("Century Gothic", 12), bg="#FF5757")
back.place(relx=0.5, y=350, anchor=tk.CENTER)
w.mainloop()