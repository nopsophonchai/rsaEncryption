from math import log2,floor,ceil
from utility import effModuloExp,binaryToString,deciToBin

def removePadding(m):
    index = 0
    if m[-1] == '1':
        return m
    for i in range(1,len(m)):
        if m[-i] == "1":
            index = -i
            break
    return m[:index]

def decrypt(d,n,m):
    blockSize = ceil(log2(n))
    newBlockSize = floor(log2(n))
    binMsg = m
    partitionedMsg = []
    for i in range(0,len(binMsg),blockSize):
        partitionedMsg.append(binMsg[i:i+blockSize])
    decryptedMsg = []
    for i in partitionedMsg:
        decrypted = effModuloExp(i,d,n)
        decryptedToBin = deciToBin(decrypted,newBlockSize)
        
        decryptedMsg.append(decryptedToBin)
    decryptedMsg[-1] = removePadding(decryptedMsg[-1])
    decryptedString = ""
    for i in decryptedMsg:
        decryptedString += i
    return binaryToString(decryptedString)



