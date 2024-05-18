import tkinter as tk
import customtkinter
from tkinter import scrolledtext
import SendEmail
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk(fg_color='grey')
app.geometry("600x440")
app.title('Connect to server')
frame = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
LoginText = customtkinter.CTkLabel(master=frame, text="Connect to server", font=('Century Gothic', 40))
LoginText.place(relx=0.5, y=75, anchor=tk.CENTER)
Abutton = tk.Button(master=frame, width=6, height=1, text="A", font=("Century Gothic", 20), bg="#0097B2",fg="white")
Abutton.place(relx=0.2, y=175, anchor=tk.CENTER)
#Signupbutton = customtkinter.CTkButton(master=frame, width=75, height=75, text="Signup", corner_radius=6)
#Signupbutton.place(relx=0.65, y=175, anchor=tk.CENTER)
Bbutton = tk.Button(master=frame, width=6, height=1, text="B", font=("Century Gothic", 20), bg="#FF5757",fg="white")
Bbutton.place(relx=0.5, y=175, anchor=tk.CENTER)
Cbutton = tk.Button(master=frame, width=6, height=1, text="C", font=("Century Gothic", 20), bg="#FF914D",fg="white")
Cbutton.place(relx=0.80, y=175, anchor=tk.CENTER)
app.mainloop()