import hashlib
import encryptor
import decryptor

def hashPassword(password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    hashedPassword = sha1.hexdigest()
    return hashedPassword



clientSelect = input("Choose your client:\tA\tB\tC\n")
if clientSelect in ['A','a']:
    with open('Akeys','r') as file:
        # print(file.readlines())
        e, d, n = file.readlines()[0].split(',')
        user = 'A'
        print(f'{e} {d} {n}')
elif clientSelect in ['B','b']:
    with open('Bkeys','r') as file:
        # print(file.readlines())
        e, d, n = file.readlines()[0].split(',')
        user = 'B'
        print(f'{e} {d} {n}')
elif clientSelect in ['C','c']:
    with open('Ckeys','r') as file:
        # print(file.readlines())
        e, d, n = file.readlines()[0].split(',')
        user = 'C'
        print(f'{e} {d} {n}')
e = int(e)
d = int(d)
n = int(n)
optionSignup = 0
# while optionSignup != 'exit':
optionSignup = input("Please type login or signup: ")
if optionSignup == 'login':
    username = input("Login: ")
    with open('shadow.txt', 'r') as file:
        for i in file.readlines():
            i = i.split(',')
            usrName, passW = i[0],i[1]
            # print(f'{usrName},{passW}')
            if username == usrName:
                password = input("Password: ")
                with open('authentication.txt','w') as file:
                    hashedPassword = hashPassword(password)
                    payload = f'{user}\t{password}\t{encryptor.encrypt(d,n,hashedPassword)}'
                    file.write(payload)

                with open('authentication.txt','r') as file:
                    currentUser,m,hashM = file.readlines()[0].split('\t')
                    with open('publicKeys.txt','r') as file:
                        for i in file.readlines():
                            i = i.split(',')
                            name,public,nNUmber = i
                            public,nNUmber = int(public),int(nNUmber)
                            if currentUser == name:
                                mDigest = decryptor.decrypt(public,nNUmber,hashM)
                                print(mDigest)

            else:
                print('Username does not exist!')


                # if passW == password:
                #     print(f'Login successful, welcome {username}!')
                #     choices = input('To send an email, type "a"\nTo view your emails, type "b"\nInput:')

        
        


    

   
                    
elif optionSignup == 'signup':
    username = input("Username: ")
    password = input("Password: ")
    with open('shadow.txt', 'a') as file:
        file.write(f'{username},{password}\n')
