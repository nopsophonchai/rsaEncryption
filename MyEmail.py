import tkinter as tk
import customtkinter
from tkinter import scrolledtext
app = customtkinter.CTk(fg_color='grey')
app.geometry("360x360")
app.title('LisofMyEmail')
ViewEmailframe = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=0, fg_color='#FFF0D3')
ViewEmailframe.place_forget()
ViewEmailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
Welcome = customtkinter.CTkLabel(master=ViewEmailframe, text="My Email", font=('Century Gothic', 20,'bold'),text_color="#441b07")
Welcome.place(relx=0.5, y=20, anchor=tk.CENTER)
text_box_frame = customtkinter.CTkFrame(master=ViewEmailframe,)
text_box_frame.place(relx=0.5, rely=0.48, anchor=tk.CENTER)
scrollbar = tk.Scrollbar(text_box_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box = customtkinter.CTkTextbox(text_box_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD, width=320, height=260)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
scrollbar.config(command=text_box.yview)
back = customtkinter.CTkButton(master=ViewEmailframe, width=100, height=30, text="Back", font=("Century Gothic", 12, 'bold'), fg_color="#FF5757", text_color="white", command=lambda: print("Back button pressed"))
back.place(relx=0.5, y=330, anchor=tk.CENTER)


app.mainloop()