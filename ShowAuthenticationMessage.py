import tkinter as tk
import customtkinter
from tkinter import scrolledtext
import SendEmail
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk(fg_color='grey')
app.geometry("600x440")
app.title('Authenticated!!!!')
AuthenMsg = tk.Label(master=app, text="MAC:.....", font=('Century Gothic', 45))
AuthenMsg.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
app.mainloop()