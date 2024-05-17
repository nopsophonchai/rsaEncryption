import tkinter as tk
import customtkinter
from tkinter import scrolledtext
import SendEmail
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk(fg_color='grey')
app.geometry("600x440")
app.title('Authenticated!!!!')
frame = customtkinter.CTkFrame(master=app, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#, y=45
LoginText = customtkinter.CTkLabel(master=frame, text="Welcome", font=('Century Gothic', 30))
LoginText.place(relx=0.5,rely=0.15, anchor=tk.CENTER)
Loginbutton = tk.Button(master=frame, width=15, height=5, text="Send Email", font=("Century Gothic", 12), bg="#0097B2")
Loginbutton.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

Signupbutton = tk.Button(master=frame, width=15, height=5, text="View Email", font=("Century Gothic", 12), bg="#FF5757")
Signupbutton.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
app.mainloop()