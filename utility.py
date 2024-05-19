def OneAndZeroes(blockSize, numLen):
    paddingNeeded = blockSize - numLen
    zeroes = "0" * (paddingNeeded - 1)
    padding = "1" + zeroes
    return padding


def deciToBin(m, bits=None):
    binary = bin(m)[2:]
    if bits:
        return binary.zfill(bits)
    return binary

def decimalToBinary(m):
    return "{0:b}".format(int(m))

def stringToBinary(m):
    strAscii = [ord(char) for char in m]
    asciiBin = [bin(asc)[2:].zfill(8) for asc in strAscii]
    concatBin = "".join(asciiBin)
    return concatBin
def binaryToString(m):
    n = 8
    bins = [m[i:i + n] for i in range(0, len(m), n)]
    asciis = [int(chunk, 2) for chunk in bins]
    chars = [chr(asciiVals) for asciiVals in asciis]
    return "".join(chars)
def effModuloExp(a,m,n):
    bits = bin(m)[2:]
    d = 1
    for bi in bits:
        d = d*d %n
        if bi != "0":
            d = (d*int(a,2)) % n 
    return d

def strToBin(string):
    strToAscii = [ord(char) for char in string]
    AsciiToBin = [bin(asc) for asc in strToAscii]
    ConcatBin = ""
    for i in AsciiToBin:
        ConcatBin += i[2:]
    return ConcatBin

def detectBin(n):
    return all(c in '01' for c in n)



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
    # print(Client)
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
   