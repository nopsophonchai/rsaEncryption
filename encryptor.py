from math import log2,floor,ceil
from utility import OneAndZeroes,decimalToBinary,effModuloExp,detectBin,stringToBinary

def encrypt(e,n,m):
    blockSize = floor(log2(n))
    binMsg = m if detectBin(m) else stringToBinary(m)
    partitionedMsg = []
    for i in range(0,len(binMsg),blockSize):
        if i+blockSize > len(binMsg):
            partitionedMsg.append(binMsg[i:]+OneAndZeroes(blockSize,len(binMsg[i:])))
        else:
            partitionedMsg.append(binMsg[i:i+blockSize])
    encryptedMsg = []
    newBlockSize = ceil(log2(n))      
    for i in partitionedMsg:
        encrypted = effModuloExp(i,e,n)
        encryptedToBin = decimalToBinary(encrypted)
        if len(encryptedToBin) < newBlockSize:
            zeroes = newBlockSize - len(encryptedToBin)
            encryptedToBin = "0"*zeroes+encryptedToBin
        encryptedMsg.append(encryptedToBin)
    encryptedString = ""
    for i in encryptedMsg:
        encryptedString += i
    return encryptedString

print(encrypt(18201807221715,18320110616131,'Hello'))
