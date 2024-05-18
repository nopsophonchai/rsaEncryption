import tkinter as tk
import customtkinter
from tkinter import scrolledtext
import SendEmail
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk(fg_color='grey')
app.geometry("600x440")
app.title('Log in')

show_password = tk.BooleanVar()
show_password.set(False)
def openanother():
    app.destroy()
    SendEmail.MainApp()
def button_function():
    openanother()
    
def toggle_password_visibility():
    global show_password
    if show_password.get():
        PWBox.configure(show="")
    else:
        PWBox.configure(show="*")

frame = customtkinter.CTkFrame(master=app, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

LoginText = customtkinter.CTkLabel(master=frame, text="Log in", font=('Century Gothic', 20))
LoginText.place(relx=0.5, y=45,anchor=tk.CENTER)

EmailLabel = customtkinter.CTkLabel(master=frame, text="Username:", font=('Century Gothic', 15))
EmailLabel.place(x=50, y=80)

EmailBox = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
EmailBox.place(x=50, y=110)

PWLabel = customtkinter.CTkLabel(master=frame, text="Password:", font=('Century Gothic', 15))
PWLabel.place(x=50, y=145)

ShowOrHide = customtkinter.CTkCheckBox(master=frame, text="Show Password", font=('Century Gothic', 10), variable=show_password, command=toggle_password_visibility)
ShowOrHide.place(x=50, y=210)

PWBox = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
PWBox.place(x=50, y=175)


#Loginbutton = customtkinter.CTkButton(master=frame, width=220, text="Login", command=button_function, corner_radius=6)
#Loginbutton.place(x=50, y=240) 
Loginbutton = tk.Button(master=frame, width=23, height=2, text="Login", font=("Century Gothic", 12), bg="#0097B2", command=button_function,fg="white")
Loginbutton.place(relx=0.5, y=270, anchor=tk.CENTER)

app.mainloop()