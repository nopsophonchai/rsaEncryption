import tkinter as tk
import customtkinter
from tkinter import scrolledtext
import SendEmail
import hashlib
import encryptor,decryptor,symmetrickeyencrypt
import random as rd
from datetime import datetime
from tkinter import messagebox

#For code simplicity, these are the session variables
Client = '' #The client computer that the user is using (NOT EMAIL ACCOUNT!)
frames = {} #Dictionary for changing frames (We have two methods to change frames since we divided the frontend between two people)
myE,myD,myN = 0,0,0  #Public, Private, N, of the Client
keys = [] #The public keys of everyone 
sE, sN, sD = 0,0,0 #Public, Private, N of Server. The server does not have access to Client's private key and vice versa

#Changing Frames(Page)
def changeFrame(frameName):
    frame = frames[frameName]
    frame.tkraise()

#Initializing: obtaining and assigning the keys to everyone
def getKey(client):
    global myE,myD,myN,sE,sN,keys,Client
    Client = client
    path = f"{client}keys.txt"
    with open(path,'r') as file:
        myE,myD,myN = map(int, file.readline().strip().split(',')) #Client Keys
    with open('publicKeys.txt','r') as file:
        keys = file.readlines()        #Public Keys
        for i in keys:
            i = i.strip().split(',')
            if i[0] == 'S':            #Obtaining server keys used only for client
                sE = int(i[1])
                sN = int(i[2])

#When user chose the client to access
def clientClick(frameName,client):
    getKey(client)
    changeFrame(frameName)
    
#Client authenticating to the Server, this is done through a button since we do not have to switch between two python scripts
def authenticate(d,n,skey,sn,frameName):
    global payLoad
    #Hashing a nonce for MAC
    shaObject = hashlib.sha256()
    nonce = f'{rd.randint(1,128)}'
    shaObject.update(nonce.encode('utf-8'))
    #Creating the MAC
    macText = shaObject.hexdigest()
    macText = encryptor.encrypt(d,n,macText) #We are signing mac with client signature
    #Making the payload for authentication 
    authChunk = f"{nonce},{macText}" # m,{sha256(m)}_prClient
    authChunk = encryptor.encrypt(skey,sn,authChunk) # {m,{sha256(m)}_prClient}_puServer This is to make sure that only server has access
    payLoad = f"{Client},{authChunk}" #Adding Client to let server know which key to use
    changeFrame(frameName)

#Server authenticate from the previous function ***THIS IS THE SERVER'S PERSPECTIVE***
def serverAuth(payload):
    global sE, sD, sN
    #Server logs for each payload that comes into the server
    with open('authentication.txt','a') as file:
        file.write(f'Client: {payload}')
        
    #Obtaining the keys for the server
    with open('Skeys.txt','r') as file:
        sE, sD, sN = map(int, file.readline().strip().split(','))
    payload = payload.split(',')
    client = payload[0]
    macChunk = payload[1]
    macChunk = decryptor.decrypt(sD,sN,macChunk)    #Decrypting the payload along with obtaining the MAC
    with open('authentication.txt','a') as file:
        file.write(f'Client Decrypted: {macChunk}') #Writing what the server decrypted into the logs
        
    #Obtaining the m and digital signature MAC
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
    #If the mac that we obtainined matches the hashed version of the m, then we grant access to the server
    if mac == nonceHash:
        changeFrame('login')
    #Add what the server obtained into the logs
    with open('authentication.txt','a') as file:
        file.write(f'Server Decrypted: {nonceHash}')
        file.write(f'Received MAC: {mac}')

#Redirecting user to sending email page
def SendEmail():
    frame2.place_forget()
    ViewEmailframe.place_forget()
    login.place_forget()
    showAuthentication.place_forget()
    serverFrame.place_forget()
    LoginText.place_forget()
    frame.place_forget()
    SendMailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#Going back to the main page
def back_to_main_frame():
    SendMailframe.place_forget()
    ViewEmailframe.place_forget()
    frame2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


#Sending the mails
def sendMail():
    #Obtaining the destination and the body from the text box
    to = Toentry.get()
    body = entry44.get("1.0", tk.END).strip()
    #Generating random number to use as synchronous key
    sssk = rd.randint(1,100000000)
    ssskByte = sssk.to_bytes(16, byteorder='big')
    ssskString = f"{sssk}"

    #Obtaining the public key of the receiver
    for i in keys:
        i = i.strip().split(',')
        if i[0] == f'{to}':
            receiverE = int(i[1])
            receiverN = int(i[2])

    #hashing the body as per PGP requirements
    shaOb = hashlib.sha256()
    shaOb.update(body.encode('utf-8'))
    digiSig = shaOb.hexdigest()
    digiSig = encryptor.encrypt(sD,sN,digiSig) #Digital signature

    bodyEncrypted = symmetrickeyencrypt.encrypt_message(body,ssskByte) #Encrypted body message

    sssKEncrypted = encryptor.encrypt(receiverE,receiverN,ssskString) #Encrypted session key for the receiver to decrypt

    #Sending to one of the client's computer We are using a mailbox file to act like an email database
    if to in ['A','B','C']:
        with open(f'{to}_mailbox.txt','a') as file:
            file.write(f'{Client},{sssKEncrypted},{digiSig},{bodyEncrypted},{datetime.now().strftime("%Y-%m-%d")}\n')
    SendMailframe.place_forget()
    ViewEmailframe.place_forget()
    frame2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

#Obtaining the mails
mails = []
def getMail():
    global mails
    with open(f'{Client}_mailbox.txt','r') as file: #Checking all of the emails in the file
        for i in file.readlines():
            i = i.strip().split(',')
            #Decryption 
            sender, sssKEncrypted, digiSig, bodyEncrypted, time = i
            sssk = decryptor.decrypt(myD,myN,sssKEncrypted)
            body = symmetrickeyencrypt.decrypt_message(bodyEncrypted,int(sssk).to_bytes(16, byteorder='big'))

            #Decrypting the digital signature with the server's keys to obtain the hashed body for authentication
            digiSig = decryptor.decrypt(sE,sN,digiSig)
            shaOb = hashlib.sha256()
            shaOb.update(body.encode('utf-8')) #Hashing the body obtained from the message
            comparator = shaOb.hexdigest()
            #***THERE IS APPARENTLY A BUG WITH THE WAY AES HASH AND PADDINGS INTERACT, WE ARE COMPARING THE FIRST 63 LETTERS 
            if digiSig[:-1] == comparator[:-1]: #If the hashed body matches the digital signature, then show it in the mailbox
                print('pass')
                mails.append(f"{sender}\n{body}\n{time}\n----------\n")

#Showing the mails from the previous functions in the interface
def showMails():
    frame2.place_forget()
    login.place_forget()
    
    showAuthentication.place_forget()
    serverFrame.place_forget()
    LoginText.place_forget()
    frame.place_forget()
    getMail()
    textBox.configure(state=tk.NORMAL)  
    textBox.delete(1.0, tk.END)
    for mail in mails:
        textBox.insert(tk.END, mail)
    textBox.configure(state=tk.DISABLED) 
    ViewEmailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk(fg_color='grey')
screenWidth = app.winfo_screenwidth()
screenHeight = app.winfo_screenheight()
x = (screenWidth // 2) - (360 // 2)
y = (screenHeight // 2) - (360 // 2)
app.geometry(f"360x360+{x}+{y}")
app.title('Choose your client')
frame = customtkinter.CTkFrame(master=app, width=360, height=360,fg_color="#FFF0D3")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

frames['main'] = frame

LoginText = customtkinter.CTkLabel(master=frame, text="Email Simulator", font=('Century Gothic', 30,'bold'),text_color="#441b07")
LoginText.place(relx=0.5, y=45, anchor=tk.CENTER)
EmailLabel = customtkinter.CTkLabel(master=frame, text="Please choose your client", font=('Century Gothic', 20,'bold'),text_color='#441b07')
EmailLabel.place(relx=0.5, y=85, anchor=tk.CENTER)
Abutton = customtkinter.CTkButton(master=frame, width=120, height=1, text="A", font=("Century Gothic", 20,'bold'), text_color="white",fg_color="#0097B2",command=lambda: clientClick('authentication', "A"))
Abutton.place(x=60, y=250, anchor=tk.CENTER)
Bbutton = customtkinter.CTkButton(master=frame, width=120, height=1, text="B", font=("Century Gothic", 20,'bold'), text_color="white",fg_color="#ff5757",command=lambda: clientClick('authentication', "B"))
Bbutton.place(x=180, y=250, anchor=tk.CENTER)
Cbutton = customtkinter.CTkButton(master=frame, width=120, height=1, text="C", font=("Century Gothic", 20,'bold'), text_color="white",fg_color="#ff914d",command=lambda: clientClick('authentication', "C"))
Cbutton.place(x=300, y=250, anchor=tk.CENTER)




serverFrame = customtkinter.CTkFrame(master=app, width=360, height=360, fg_color="#FFF0D3")
serverFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
LoginText = customtkinter.CTkLabel(master=serverFrame, text="Connect to server", font=('Century Gothic', 20,'bold'),text_color="#441b07")
LoginText.place(relx=0.5, y=75, anchor=tk.CENTER)
Abutton = customtkinter.CTkButton(master=serverFrame, width=200, height=40, text="Confirm", font=("Century Gothic", 20,'bold'), fg_color="#0097B2", text_color="white", command=lambda: authenticate(myD, myN, sE, sN, 'showAuth'))
Abutton.place(relx=0.5, y=205, anchor=tk.CENTER)

frames['authentication'] = serverFrame

showAuthentication = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=0, fg_color="#FFF0D3")
showAuthentication.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
demoText = customtkinter.CTkLabel(master=showAuthentication, text="Client->Server: Client,{m,{hash(m)}_prClient}_puServer", font=('Century Gothic', 12,'bold'),text_color='#441b07')
demoText.place(relx=0.5, y=75, anchor=tk.CENTER)
Authbutton = customtkinter.CTkButton(master=showAuthentication, width=200, height=40, text="Authenticate", font=("Century Gothic", 15,'bold'), text_color="white",fg_color="#ff5757",command=lambda: serverAuth(payLoad))
Authbutton.place(relx=0.5, y=205, anchor=tk.CENTER)

frames['showAuth'] = showAuthentication

#Logging into the system, in this particular case, the server only has one account assumed to be known by all humans accessing
#The password and username is stored in cleartext in shadow.txt for ease of understanding 
def authLogin():
    #We are simulating the sender side
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
    with open('shadow.txt','r') as file:
        realUse,realPass = file.readlines()[0].strip().split(',')
        if realUse == use: 
            shaOb = hashlib.sha256()
            shaOb.update(realPass.encode('utf-8'))
            realPass = shaOb.hexdigest()
            if realPass == passW:  #If the hashed version of the password obtained by shadow.txt matches the hashed password from the user
                changeFrame('frame2')
                
    

login = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=0, fg_color="#FFF0D3")
login.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
LoginText = customtkinter.CTkLabel(master=login, text="Log in", font=('Century Gothic', 20,'bold'),text_color="#441b07")
LoginText.place(relx=0.5, y=45,anchor=tk.CENTER)
EmailLabel = customtkinter.CTkLabel(master=login, text="Username:", font=('Century Gothic', 15,'bold'),text_color="#441b07")
EmailLabel.place(relx=0.5, y=90,anchor=tk.CENTER)
EmailBox = customtkinter.CTkEntry(master=login, width=220, placeholder_text='Username')
EmailBox.place(relx=0.5, y=120,anchor=tk.CENTER)
PWLabel = customtkinter.CTkLabel(master=login, text="Password:", font=('Century Gothic', 15,'bold'),text_color="#441b07")
PWLabel.place(relx=0.5, y=155,anchor=tk.CENTER)
PWBox = customtkinter.CTkEntry(master=login, width=220, placeholder_text='Password', show="*")
PWBox.place(relx=0.5, y=185,anchor=tk.CENTER)
Loginbutton = customtkinter.CTkButton(master=login, width=200, height=40, corner_radius=15,text="Login", font=("Century Gothic", 15,'bold'), fg_color="#ff914d",text_color="white", command= lambda: authLogin())
Loginbutton.place(relx=0.5, y=250, anchor=tk.CENTER)

frames['login'] = login
def logout():
    messagebox.showinfo("Logged Out", "You have been logged out.")
    app.destroy()
frame2 = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=0,fg_color="#FFF0D3")
frame2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
LoginText = customtkinter.CTkLabel(master=frame2, text="Welcome", font=('Century Gothic', 30,'bold'),text_color="#441b07")
LoginText.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
Loginbutton = customtkinter.CTkButton(master=frame2, width=250, height=80, text="Send Email", font=("Century Gothic", 12,'bold'), fg_color="#0097B2", text_color="white", command=lambda:SendEmail())
Loginbutton.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
Signupbutton = customtkinter.CTkButton(master=frame2, width=250, height=80, text="View Email", font=("Century Gothic", 12,'bold'), fg_color="#ff5757", text_color="white", command=lambda:showMails())
Signupbutton.place(relx=0.5, rely=0.60, anchor=tk.CENTER)
Logoutbutton = customtkinter.CTkButton(master=frame2, width=250, height=40, text="Logout", font=("Century Gothic", 12,'bold'), text_color="white",fg_color="#ff914d",command=lambda: logout())
Logoutbutton.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
frames['frame2'] = frame2 


SendMailframe = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=0, fg_color="#FFF0D3")
SendMailframe.place_forget()
Welcome = customtkinter.CTkLabel(master=SendMailframe, text="Send Email", font=('Century Gothic', 20,'bold'),text_color="#441b07")
Welcome.place(relx=0.5, y=25,anchor=tk.CENTER)
ToLabel = customtkinter.CTkLabel(master=SendMailframe, text="To:", font=('Century Gothic', 15,'bold'),text_color="#441b07")
ToLabel.place(relx=0.5, y=50,anchor=tk.CENTER)
Toentry = customtkinter.CTkEntry(master=SendMailframe, width=200)
Toentry.place(relx=0.5, y=75,anchor=tk.CENTER)
Bodylabel = customtkinter.CTkLabel(master=SendMailframe, text="Body:", font=('Century Gothic', 15,'bold'),text_color="#441b07")
Bodylabel.place(relx=0.5, y=110,anchor=tk.CENTER)
entry44 = scrolledtext.ScrolledText(master=SendMailframe, width=40, height=8, font=("Times New Roman", 15))
entry44.place(relx=0.5, y=200,anchor=tk.CENTER)
send = customtkinter.CTkButton(master=SendMailframe, width=100, height=30, text="Send", font=("Century Gothic", 12,'bold'), fg_color="#0097B2", text_color="white",command=lambda:sendMail())
send.place(relx=0.3, y=310,anchor=tk.CENTER)
back = customtkinter.CTkButton(master=SendMailframe, width=100, height=30, text="Back", font=("Century Gothic", 12,'bold'), fg_color="#FF5757", text_color="white", command=lambda: back_to_main_frame())
back.place(relx=0.7, y=310,anchor=tk.CENTER)





ViewEmailframe = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=0, fg_color='#FFF0D3')
ViewEmailframe.place_forget()
ViewEmailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
Welcome = customtkinter.CTkLabel(master=ViewEmailframe, text="My Email", font=('Century Gothic', 20,'bold'),text_color="#441b07")
Welcome.place(relx=0.5, y=20, anchor=tk.CENTER)
textBoxFrame = customtkinter.CTkFrame(master=ViewEmailframe,)
textBoxFrame.place(relx=0.5, rely=0.48, anchor=tk.CENTER)
scrollbar = tk.Scrollbar(textBoxFrame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
textBox = customtkinter.CTkTextbox(textBoxFrame, yscrollcommand=scrollbar.set, wrap=tk.WORD, width=320, height=260)
textBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
scrollbar.config(command=textBox.yview)
back = customtkinter.CTkButton(master=ViewEmailframe, width=100, height=30, text="Back", font=("Century Gothic", 12, 'bold'), fg_color="#FF5757", text_color="white", command=lambda: back_to_main_frame())
back.place(relx=0.5, y=330, anchor=tk.CENTER)

changeFrame("main")

app.mainloop()