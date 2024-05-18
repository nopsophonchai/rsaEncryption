import tkinter as tk
import customtkinter
from tkinter import scrolledtext
import SendEmail
import hashlib
import encryptor,decryptor
import random as rd

Client = ''
frames = {}
myE,myD,myN = 0,0,0
keys = []
sE, sN, sD = 0,0,0
def changeFrame(frameName):
    frame = frames[frameName]
    frame.tkraise()
def getKey(client):
    global myE,myD,myN,sE,sN,keys,Client
    Client = client
    path = f"{client}keys.txt"
    with open(path,'r') as file:
        myE,myD,myN = map(int, file.readline().strip().split(','))
    with open('publicKeys.txt','r') as file:
        keys = file.readlines()
        for i in keys:
            i = i.strip().split(',')
            if i[0] == 'S':
                sE = int(i[1])
                sN = int(i[2])
def clientClick(frameName,client):
    getKey(client)
    keytext = f"e = {myE} d = {myD} n = {myN}"
    keyText.configure(text=keytext)
    changeFrame(frameName)
    
def authenticate(d,n,skey,sn,frameName):
    global payLoad
    print(Client)
    shaObject = hashlib.sha256()
    nonce = f'{rd.randint(1,128)}'
    shaObject.update(nonce.encode('utf-8'))
    macText = shaObject.hexdigest()
    macText = encryptor.encrypt(d,n,macText) #We are signing mac with client signature
    authChunk = f"{nonce},{macText}"
    authChunk = encryptor.encrypt(skey,sn,authChunk)
    payLoad = f"{Client},{authChunk}"
    # print(payLoad)
    # authText.configure(text=payLoad)
    changeFrame(frameName)
def serverAuth(payload):
    global sE, sD, sN
    with open('authentication.txt','a') as file:
        file.write(f'Client: {payload}')
        
    with open('Skeys.txt','r') as file:
        sE, sD, sN = map(int, file.readline().strip().split(','))
    payload = payload.split(',')
    client = payload[0]
    macChunk = payload[1]
    macChunk = decryptor.decrypt(sD,sN,macChunk)
    with open('authentication.txt','a') as file:
        file.write(f'Client Decrypted: {macChunk}')
        
    macChunk = macChunk.split(',')
    for i in keys:
        i = i.strip().split(',')
        if i[0] == client:
            cE = int(i[1])
            cN = int(i[2])
    nonce = macChunk[0]
    mac = decryptor.decrypt(cE,cN,macChunk[1])
    shaObject = hashlib.sha256()
    shaObject.update(nonce.encode('utf-8'))
    nonceHash = shaObject.hexdigest()
    if mac == nonceHash:
        changeFrame('login')
    with open('authentication.txt','a') as file:
        file.write(f'Server Decrypted: {nonceHash}')
        file.write(f'Received MAC: {mac}')
        
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk(fg_color='grey')
app.geometry("600x440")
app.title('Choose your client')
frame = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

frames['main'] = frame

LoginText = customtkinter.CTkLabel(master=frame, text="Email Simulator", font=('Century Gothic', 30))
LoginText.place(relx=0.5, y=45, anchor=tk.CENTER)
EmailLabel = customtkinter.CTkLabel(master=frame, text="Please choose your client", font=('Century Gothic', 20))
EmailLabel.place(relx=0.5, y=85, anchor=tk.CENTER)
#Loginbutton = customtkinter.CTkButton(master=frame, width=75, height=75, text="Login", corner_radius=6)
#Loginbutton.place(relx=0.35, y=175, anchor=tk.CENTER)
Abutton = tk.Button(master=frame, width=6, height=1, text="A", font=("Century Gothic", 20), bg="#0097B2",fg="white",command=lambda: clientClick('authentication', "A"))
Abutton.place(relx=0.2, y=175, anchor=tk.CENTER)
#Signupbutton = customtkinter.CTkButton(master=frame, width=75, height=75, text="Signup", corner_radius=6)
#Signupbutton.place(relx=0.65, y=175, anchor=tk.CENTER)
Bbutton = tk.Button(master=frame, width=6, height=1, text="B", font=("Century Gothic", 20), bg="#FF5757",fg="white",command=lambda: clientClick('authentication', "B"))
Bbutton.place(relx=0.5, y=175, anchor=tk.CENTER)
Cbutton = tk.Button(master=frame, width=6, height=1, text="C", font=("Century Gothic", 20), bg="#FF914D",fg="white",command=lambda: clientClick('authentication', "C"))
Cbutton.place(relx=0.80, y=175, anchor=tk.CENTER)




serverFrame = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=15)
serverFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
LoginText = customtkinter.CTkLabel(master=serverFrame, text="Connect to server", font=('Century Gothic', 40))
LoginText.place(relx=0.5, y=75, anchor=tk.CENTER)
Abutton = tk.Button(master=serverFrame, width=6, height=1, text="A", font=("Century Gothic", 20), bg="#0097B2",fg="white",command=lambda: authenticate(myD,myN,sE,sN,'showAuth'))
Abutton.place(relx=0.2, y=175, anchor=tk.CENTER)
keyText = customtkinter.CTkLabel(master=serverFrame, text=f"e = {myE} d = {myD} n = {myN}", font=('Century Gothic', 40))
keyText.place(relx=0.5, y=225, anchor=tk.CENTER)
#Signupbutton = customtkinter.CTkButton(master=frame, width=75, height=75, text="Signup", corner_radius=6)
#Signupbutton.place(relx=0.65, y=175, anchor=tk.CENTER)
# Bbutton = tk.Button(master=serverFrame, width=6, height=1, text="B", font=("Century Gothic", 20), bg="#FF5757",fg="white")
# Bbutton.place(relx=0.5, y=175, anchor=tk.CENTER)
# Cbutton = tk.Button(master=serverFrame, width=6, height=1, text="C", font=("Century Gothic", 20), bg="#FF914D",fg="white")
# Cbutton.place(relx=0.80, y=175, anchor=tk.CENTER)


frames['authentication'] = serverFrame

showAuthentication = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=15)
showAuthentication.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
demoText = customtkinter.CTkLabel(master=showAuthentication, text="Client->Server: Client,{m,{hash(m)}_prClient}_puServer", font=('Century Gothic', 12))
demoText.place(relx=0.5, y=175, anchor=tk.CENTER)
Authbutton = tk.Button(master=showAuthentication, width=6, height=1, text="Authenticate", font=("Century Gothic", 20), bg="#0097B2",fg="white",command=lambda: serverAuth(payLoad))
Authbutton.place(relx=0.2, y=250, anchor=tk.CENTER)

frames['showAuth'] = showAuthentication

def authLogin():
    #We are simulating the sender side
    print(sN)
    username = EmailBox.get()
    password = PWBox.get()
    shaOb = hashlib.sha256()
    shaOb.update(password.encode('utf-8'))
    password = shaOb.hexdigest()
    username = encryptor.encrypt(sE,sN,username)
    password = encryptor.encrypt(sE,sN,password)
    with open("Login.txt",'w') as file:
        file.write(f"{username},{password}")
    #Simulating the receiver side
    with open('Login.txt','r') as file:
        use,passW = file.readlines()[0].strip().split(',')
        use = decryptor.decrypt(sD,sN,use)
        passW = decryptor.decrypt(sD,sN,passW)
        print(f'{use},{passW}')
    with open('shadow.txt','r') as file:
        realUse,realPass = file.readlines()[0].strip().split(',')
        
        if realUse == use:
            shaOb = hashlib.sha256()
            shaOb.update(realPass.encode('utf-8'))
            realPass = shaOb.hexdigest()
            print(f'{realUse},{realPass}')
            if realPass == passW:
                changeFrame('menu')

login = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=15)
login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
LoginText = customtkinter.CTkLabel(master=login, text="Log in", font=('Century Gothic', 20))
LoginText.place(relx=0.5, y=45,anchor=tk.CENTER)
EmailLabel = customtkinter.CTkLabel(master=login, text="Username:", font=('Century Gothic', 15))
EmailLabel.place(x=50, y=80)
EmailBox = customtkinter.CTkEntry(master=login, width=220, placeholder_text='Username')
EmailBox.place(x=50, y=110)
PWLabel = customtkinter.CTkLabel(master=login, text="Password:", font=('Century Gothic', 15))
PWLabel.place(x=50, y=145)
PWBox = customtkinter.CTkEntry(master=login, width=220, placeholder_text='Password', show="*")
PWBox.place(x=50, y=175)
Loginbutton = tk.Button(master=login, width=15, height=5, text="Send Email", font=("Century Gothic", 12), bg="#0097B2",fg="white", command= lambda: authLogin())
Loginbutton.place(x=50, y=225, anchor=tk.CENTER)

frames['login'] = login

menu = customtkinter.CTkFrame(master=app, width=320, height=360, corner_radius=15)
menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
#, y=45
LoginText = customtkinter.CTkLabel(master=menu, text="Welcome", font=('Century Gothic', 30))
LoginText.place(relx=0.5,rely=0.15, anchor=tk.CENTER)
Loginbutton = tk.Button(master=menu, width=15, height=5, text="Send Email", font=("Century Gothic", 12), bg="#0097B2",fg="white")
Loginbutton.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

Signupbutton = tk.Button(master=menu, width=15, height=5, text="View Email", font=("Century Gothic", 12), bg="#FF5757",fg="white")
Signupbutton.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

frames['menu'] = menu


changeFrame("main")


app.mainloop()