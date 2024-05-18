from math import log2,floor,ceil
from utility import OneAndZeroes,decimalToBinary,effModuloExp,detectBin,stringToBinary,binaryToString,strToBin
import random as rd
import hashlib
from decryptor import decrypt

def encrypt(e,n,m):
    blockSize = floor(log2(n))
    binMsg = m if detectBin(m) else stringToBinary(m)
    # print(len(binMsg))
    # print(binMsg)

    
    partitionedMsg = []
    for i in range(0,len(binMsg),blockSize):
        if i+blockSize > len(binMsg):
            partitionedMsg.append(binMsg[i:]+OneAndZeroes(blockSize,len(binMsg[i:])))
        else:
            partitionedMsg.append(binMsg[i:i+blockSize])
    encryptedMsg = []
    newBlockSize = ceil(log2(n))
    for i in partitionedMsg:
        # print(len(i))
        encrypted = effModuloExp(i,e,n)
        encryptedToBin = decimalToBinary(encrypted)
        # print(len(encryptedToBin))
        if len(encryptedToBin) < newBlockSize:
            zeroes = newBlockSize - len(encryptedToBin)
            encryptedToBin = "0"*zeroes+encryptedToBin
        encryptedMsg.append(encryptedToBin)
    encryptedString = ""
    for i in encryptedMsg:
        encryptedString += i
    return encryptedString

# 50467,187741
shaObject = hashlib.sha256()
nonce = f'{rd.randint(1,128)}'
shaObject.update(nonce.encode('utf-8'))
macText = shaObject.hexdigest()
macText = encrypt(50467,187741,macText) #We are signing mac with client signature
# print(macText)
authChunk = f"{nonce},{macText}"
print(authChunk)
authChunk = encrypt(50467,187741,authChunk)
# print(authChunk)
print(decrypt(168331,187741,authChunk))