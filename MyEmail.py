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
ToLabel = customtkinter.CTkLabel(master=SendMailframe, text="From:", font=('Century Gothic', 15))
ToLabel.place(x=25, y=80)
Toentry = customtkinter.CTkEntry(master=SendMailframe, width=200)
Toentry.place(x=85, y=80)
Bodylabel = customtkinter.CTkLabel(master=SendMailframe, text="Body:", font=('Century Gothic', 15))
Bodylabel.place(x=25, y=110)
entry44 = scrolledtext.ScrolledText(master=SendMailframe,  width=23, height=8, font=("Century Gothic",15))
entry44.place(x=25, y=140)
back = tk.Button(master=SendMailframe, width=10, height=1, text="Back", font=("Century Gothic", 12), bg="#FF5757")
back.place(relx=0.5, y=350, anchor=tk.CENTER)
w.mainloop()