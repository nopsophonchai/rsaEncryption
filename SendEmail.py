import tkinter as tk
import customtkinter
from tkinter import scrolledtext
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
class MainApp:
    def __init__(self):
        self.w = customtkinter.CTk(fg_color='grey')
        self.w.geometry("600x440")
        self.w.title('Welcome')
        SendMailframe = customtkinter.CTkFrame(master=self.w, width=320, height=400, corner_radius=15,fg_color='white')
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

        send = customtkinter.CTkButton(master=SendMailframe, width=130, text="Send", corner_radius=6)
        send.place(x=25, y=360)
        clear = customtkinter.CTkButton(master=SendMailframe, width=130, text="clear", corner_radius=6)
        clear.place(x=158, y=360)

        self.w.mainloop()
if __name__ == "__main__":
    MainApp()