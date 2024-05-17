import tkinter as tk
import customtkinter
from tkinter import scrolledtext
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
class MainApp:
    def __init__(self):
        self.w = customtkinter.CTk(fg_color='grey')
        self.w.geometry("600x440")
        self.w.title('SendEmail')
        SendMailframe = customtkinter.CTkFrame(master=self.w, width=320, height=400, corner_radius=15,fg_color='white')
        SendMailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
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
        #send = customtkinter.CTkButton(master=SendMailframe, width=130, text="Send", corner_radius=6)
        #send.place(x=25, y=360)
        send = tk.Button(master=SendMailframe, width=10, height=1, text="Send", font=("Century Gothic", 12), bg="#0097B2")
        send.place(x=25, y=350)
        #clear = customtkinter.CTkButton(master=SendMailframe, width=130, text="Back", corner_radius=6)
        #clear.place(x=158, y=360)
        send = tk.Button(master=SendMailframe, width=10, height=1, text="Back", font=("Century Gothic", 12), bg="#FF5757")
        send.place(x=190, y=350)
        self.w.mainloop()
if __name__ == "__main__":
    MainApp()