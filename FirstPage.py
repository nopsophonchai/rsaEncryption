import tkinter as tk 

window =tk.Tk()
window.configure(bg='#B38E7F')
window.geometry("400x500")
window.title("Welcome Page")

label = tk.Label(window,bg='#FFCAB6', text = "Which client are you ?", font=('Arial', 18))
label.pack(padx=20, pady=50 )

ClinetA = tk.Button(window,bg='#B37F8C',text="Client A", font=('Arial', 16))
ClinetB = tk.Button(window,bg='#B37F8C',text="Client B", font=('Arial', 16))
ClinetC = tk.Button(window,bg='#B37F8C',text="Client C", font=('Arial', 16))
ClinetA.pack(padx=10,pady=10)
ClinetB.pack(padx=10,pady=10)
ClinetC.pack(padx=10,pady=10)
window.mainloop()