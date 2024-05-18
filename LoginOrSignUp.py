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
LoginText = customtkinter.CTkLabel(master=frame, text="Authenticated!", font=('Century Gothic', 30))
LoginText.place(relx=0.5, y=45, anchor=tk.CENTER)
EmailLabel = customtkinter.CTkLabel(master=frame, text="Login or Signup", font=('Century Gothic', 20))
EmailLabel.place(relx=0.5, y=85, anchor=tk.CENTER)
#Loginbutton = customtkinter.CTkButton(master=frame, width=75, height=75, text="Login", corner_radius=6)
#Loginbutton.place(relx=0.35, y=175, anchor=tk.CENTER)
Loginbutton = tk.Button(master=frame, width=6, height=1, text="Back", font=("Century Gothic", 20), bg="#0097B2",fg="white")
Loginbutton.place(relx=0.25, y=175, anchor=tk.CENTER)
#Signupbutton = customtkinter.CTkButton(master=frame, width=75, height=75, text="Signup", corner_radius=6)
#Signupbutton.place(relx=0.65, y=175, anchor=tk.CENTER)
Signupbutton = tk.Button(master=frame, width=6, height=1, text="Back", font=("Century Gothic", 20), bg="#FF5757",fg="white")
Signupbutton.place(relx=0.75, y=175, anchor=tk.CENTER)
app.mainloop()