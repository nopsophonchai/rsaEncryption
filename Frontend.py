import tkinter as tk
import customtkinter
from tkinter import scrolledtext
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk(fg_color='grey')
app.geometry("600x440")
app.title('Log in')

show_password = tk.BooleanVar()
show_password.set(False)

def button_function():
    
    app.destroy()
    w = customtkinter.CTk(fg_color='grey')
    w.geometry("600x440")
    w.title('Welcome')
    SendMailframe = customtkinter.CTkFrame(master=w, width=320, height=400, corner_radius=15,fg_color='white')
    SendMailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    Welcome = customtkinter.CTkLabel(master=SendMailframe, text="WELCOME!!!", font=('Century Gothic', 20))
    Welcome.place(x=105, y=25)
    
 
    ToLabel = customtkinter.CTkLabel(master=SendMailframe, text="To:", font=('Century Gothic', 15))
    ToLabel.place(x=25, y=80)

    Toentry = customtkinter.CTkEntry(master=SendMailframe, width=200)
    Toentry.place(x=85, y=80)

    Subjectlabel = customtkinter.CTkLabel(master=SendMailframe, text="Subject:", font=('Century Gothic', 15))
    Subjectlabel.place(x=25, y=110)

    SubjectEntry = customtkinter.CTkEntry(master=SendMailframe, width=200)
    SubjectEntry.place(x=85, y=110)

    Messagelabel = customtkinter.CTkLabel(master=SendMailframe, text="Message:", font=('Century Gothic', 15))
    Messagelabel.place(x=25, y=140)

   # entry44 = customtkinter.CTkEntry(master=anotherframe, width=260,height=170)
    #entry44.place(x=25, y=170)
    entry44 = scrolledtext.ScrolledText(master=SendMailframe,  width=25, height=8, font=("Times New Roman",15))
    entry44.place(x=25, y=170)

    send = customtkinter.CTkButton(master=SendMailframe, width=130, text="Send", command=button_function, corner_radius=6)
    send.place(x=25, y=360)
    clear = customtkinter.CTkButton(master=SendMailframe, width=130, text="clear", command=button_function, corner_radius=6)
    clear.place(x=158, y=360)

    w.mainloop()

def toggle_password_visibility():
    global show_password
    if show_password.get():
        PWBox.configure(show="")
    else:
        PWBox.configure(show="*")

frame = customtkinter.CTkFrame(master=app, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

LoginText = customtkinter.CTkLabel(master=frame, text="Log in", font=('Century Gothic', 20))
LoginText.place(x=135, y=45)

EmailLabel = customtkinter.CTkLabel(master=frame, text="Email", font=('Century Gothic', 15))
EmailLabel.place(x=55, y=80)

EmailBox = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
EmailBox.place(x=50, y=110)

PWLabel = customtkinter.CTkLabel(master=frame, text="Password", font=('Century Gothic', 15))
PWLabel.place(x=55, y=145)

ShowOrHide = customtkinter.CTkCheckBox(master=frame, text="Show Password", font=('Century Gothic', 10), variable=show_password, command=toggle_password_visibility)
ShowOrHide.place(x=50, y=210)

PWBox = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
PWBox.place(x=50, y=175)


Loginbutton = customtkinter.CTkButton(master=frame, width=220, text="Login", command=button_function, corner_radius=6)
Loginbutton.place(x=50, y=240)

app.mainloop()