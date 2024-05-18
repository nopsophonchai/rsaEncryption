import tkinter as tk
import customtkinter
from tkinter import scrolledtext

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk(fg_color='grey')
app.geometry("600x440")
app.title('Authenticated!!!!')

frame = customtkinter.CTkFrame(master=app, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


LoginText = customtkinter.CTkLabel(master=frame, text="Welcome", font=('Century Gothic', 30))
LoginText.place(relx=0.5,rely=0.15, anchor=tk.CENTER)

def SendEmail():
    frame.place_forget()
    SendMailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def back_to_main_frame():
    SendMailframe.place_forget()
    ViewEmailframe.place_forget()
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def ViewEmail():
    frame.place_forget()
    ViewEmailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

ViewEmailframe = customtkinter.CTkFrame(master=app, width=320, height=400, corner_radius=15,fg_color='white')
ViewEmailframe.place_forget()

Welcome = customtkinter.CTkLabel(master=ViewEmailframe, text="My Email", font=('Century Gothic', 20))
Welcome.place(relx=0.5, y=40,anchor=tk.CENTER)

ToLabel = customtkinter.CTkLabel(master=ViewEmailframe, text="From:", font=('Century Gothic', 15))
ToLabel.place(x=25, y=80)

Toentry = customtkinter.CTkEntry(master=ViewEmailframe, width=200)
Toentry.place(x=85, y=80)

Bodylabel = customtkinter.CTkLabel(master=ViewEmailframe, text="Body:", font=('Century Gothic', 15))
Bodylabel.place(x=25, y=110)

entry44 = scrolledtext.ScrolledText(master=ViewEmailframe,  width=23, height=8, font=("Century Gothic",15))
entry44.place(x=25, y=140)

back = tk.Button(master=ViewEmailframe, width=10, height=1, text="Back", font=("Century Gothic", 12), bg="#FF5757", fg="white", command=back_to_main_frame)
back.place(relx=0.5, y=350, anchor=tk.CENTER)


SendMailframe = customtkinter.CTkFrame(master=app, width=320, height=400, corner_radius=15,fg_color='white')
SendMailframe.place_forget()

Welcome = customtkinter.CTkLabel(master=SendMailframe, text="Send Email", font=('Century Gothic', 20))
Welcome.place(x=105, y=25)

ToLabel = customtkinter.CTkLabel(master=SendMailframe, text="To:", font=('Century Gothic', 15))
ToLabel.place(x=25, y=80)
    
Toentry = customtkinter.CTkEntry(master=SendMailframe, width=200)
Toentry.place(x=85, y=80)
    
Bodylabel = customtkinter.CTkLabel(master=SendMailframe, text="Body:", font=('Century Gothic', 15))
Bodylabel.place(x=25, y=110)
    
entry44 = scrolledtext.ScrolledText(master=SendMailframe,  width=25, height=8, font=("Times New Roman",15))
entry44.place(x=25, y=140)

send = tk.Button(master=SendMailframe, width=10, height=1, text="Send", font=("Century Gothic", 12), bg="#0097B2",fg="white")
send.place(x=25, y=350)

back = tk.Button(master=SendMailframe, width=10, height=1, text="Back", font=("Century Gothic", 12), bg="#FF5757", fg="white", command=back_to_main_frame)
back.place(x=190, y=350)



Loginbutton = tk.Button(master=frame, width=15, height=5, text="Send Email", font=("Century Gothic", 12), bg="#0097B2",fg="white",command=SendEmail)
Loginbutton.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

Signupbutton = tk.Button(master=frame, width=15, height=5, text="View Email", font=("Century Gothic", 12), bg="#FF5757",fg="white",command=ViewEmail)
Signupbutton.place(relx=0.5, rely=0.75, anchor=tk.CENTER)


app.mainloop()
