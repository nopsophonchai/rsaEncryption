import tkinter as tk
import customtkinter
from tkinter import scrolledtext
import SendEmail
import hashlib
import encryptor,decryptor,symmetrickeyencrypt
import random as rd
from datetime import datetime

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

#Viewing the emails that was sent
def ViewEmail():
    frame2.place_forget()
    frame2.place_forget()
    login.place_forget()
    showAuthentication.place_forget()
    serverFrame.place_forget()
    LoginText.place_forget()
    frame.place_forget()
    getMail()
    ViewEmailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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
    text_box.config(state=tk.NORMAL)  
    text_box.delete(1.0, tk.END)
    for mail in mails:
        text_box.insert(tk.END, mail)
    text_box.config(state=tk.DISABLED) 
    ViewEmailframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        
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
Abutton = tk.Button(master=frame, width=6, height=1, text="A", font=("Century Gothic", 20), bg="#0097B2",fg="white",command=lambda: clientClick('authentication', "A"))
Abutton.place(relx=0.2, y=175, anchor=tk.CENTER)
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

frames['authentication'] = serverFrame

showAuthentication = customtkinter.CTkFrame(master=app, width=360, height=360, corner_radius=15)
showAuthentication.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
demoText = customtkinter.CTkLabel(master=showAuthentication, text="Client->Server: Client,{m,{hash(m)}_prClient}_puServer", font=('Century Gothic', 12))
demoText.place(relx=0.5, y=175, anchor=tk.CENTER)
Authbutton = tk.Button(master=showAuthentication, width=6, height=1, text="Authenticate", font=("Century Gothic", 20), bg="#0097B2",fg="white",command=lambda: serverAuth(payLoad))
Authbutton.place(relx=0.2, y=250, anchor=tk.CENTER)

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
Loginbutton = tk.Button(master=login, width=15, height=5, text="Login", font=("Century Gothic", 12), bg="#0097B2",fg="white", command= lambda: authLogin())
Loginbutton.place(x=50, y=225, anchor=tk.CENTER)

frames['login'] = login

frame2 = customtkinter.CTkFrame(master=app, width=320, height=360, corner_radius=15)
frame2.place_forget()
frame2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
LoginText = customtkinter.CTkLabel(master=frame2, text="Welcome", font=('Century Gothic', 30))
LoginText.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
Loginbutton = tk.Button(master=frame2, width=15, height=5, text="Send Email", font=("Century Gothic", 12), bg="#0097B2", fg="white", command=SendEmail)
Loginbutton.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
Signupbutton = tk.Button(master=frame2, width=15, height=5, text="View Email", font=("Century Gothic", 12), bg="#FF5757", fg="white", command=showMails)
Signupbutton.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
frames['frame2'] = frame2 


SendMailframe = customtkinter.CTkFrame(master=app, width=320, height=400, corner_radius=15, fg_color='white')
SendMailframe.place_forget()
Welcome = customtkinter.CTkLabel(master=SendMailframe, text="Send Email", font=('Century Gothic', 20))
Welcome.place(x=105, y=25)
ToLabel = customtkinter.CTkLabel(master=SendMailframe, text="To:", font=('Century Gothic', 15))
ToLabel.place(x=25, y=80)
Toentry = customtkinter.CTkEntry(master=SendMailframe, width=200)
Toentry.place(x=85, y=80)
Bodylabel = customtkinter.CTkLabel(master=SendMailframe, text="Body:", font=('Century Gothic', 15))
Bodylabel.place(x=25, y=110)
entry44 = scrolledtext.ScrolledText(master=SendMailframe, width=25, height=8, font=("Times New Roman", 15))
entry44.place(x=150, y=170)
send = tk.Button(master=SendMailframe, width=10, height=1, text="Send", font=("Century Gothic", 12), bg="#0097B2", fg="white",command=lambda:sendMail())
send.place(x=100, y=380)
back = tk.Button(master=SendMailframe, width=10, height=1, text="Back", font=("Century Gothic", 12), bg="#FF5757", fg="white", command=back_to_main_frame)
back.place(x=260, y=380)




ViewEmailframe = customtkinter.CTkFrame(master=app, width=320, height=400, corner_radius=15, fg_color='white')
ViewEmailframe.place_forget()
Welcome = customtkinter.CTkLabel(master=ViewEmailframe, text="My Email", font=('Century Gothic', 20))
Welcome.place(relx=0.5, y=40, anchor=tk.CENTER)

text_box_frame = customtkinter.CTkFrame(master=ViewEmailframe)
text_box_frame.pack(pady=20, padx=20)
scrollbar = tk.Scrollbar(text_box_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box = tk.Text(text_box_frame, height=20, width=50, yscrollcommand=scrollbar.set)
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=text_box.yview)

back = tk.Button(master=ViewEmailframe, width=10, height=1, text="Back", font=("Century Gothic", 12), bg="#FF5757", fg="white", command=back_to_main_frame)
back.place(relx=0.5, y=400, anchor=tk.CENTER)

changeFrame("main")

app.mainloop()