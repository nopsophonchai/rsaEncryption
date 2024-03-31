from math import log2,floor,ceil
from utility import OneAndZeroes,decimalToBinary,effModuloExp,strToBin,detectBin

def encrypt(e,n,m):
    blockSize = floor(log2(n))
    binMsg = m if detectBin(m) else strToBin(m)
    partitionedMsg = []
    for i in range(0,len(binMsg),blockSize):
        if i+blockSize > len(binMsg):
            partitionedMsg.append(binMsg[i:]+OneAndZeroes(blockSize,len(binMsg[i:])))
        else:
            partitionedMsg.append(binMsg[i:i+blockSize])
    encryptedMsg = []
    newBlockSize = ceil(log2(n))
    for i in partitionedMsg:
        encrypted = effModuloExp(int(i,2),e,n)
        encryptedToBin = decimalToBinary(encrypted)
        if len(encryptedToBin) < newBlockSize:
            zeroes = newBlockSize - len(encryptedToBin)
            encryptedToBin = "0"*zeroes+encryptedToBin
        encryptedMsg.append(encryptedToBin)
    encryptedString = ""
    for i in encryptedMsg:
        encryptedString += i
    return encryptedString



print(encrypt(77,143,"1011000110101011"))
print(encrypt(77,143,"Hello"))
# print(encrypt(2699,45359,"1011000110101011"))
# padding = OneAndZeroes(7,3)
# print(padding)
# print(effModuloExp(88,77,143))
# ConcatBin = strToBin("hello")
# print(ConcatBin)

