from math import log2,floor,ceil
from utility import OneAndZeroes,decimalToBinary,effModuloExp,strToBin,detectBin,binaryToString,deciToBin
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
    # print(decryptedMsg)
    decryptedMsg[-1] = removePadding(decryptedMsg[-1])
    decryptedString = ""
    for i in decryptedMsg:
        decryptedString += i
    # print(decryptedString)
    return binaryToString(decryptedString)



# 01110101110011010111111000000100
#1011000110101011
# print(decrypt(53,143,"011110010000011001001001"))
# print(decrypt(53,143,"011011000100000001000011000001010110001100010001"))
# print(decrypt(7571,45359,"01110101110011010111111000000100"))


