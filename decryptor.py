from math import log2,floor,ceil
from utility import OneAndZeroes,decimalToBinary,effModuloExp,strToBin,detectBin
def removePadding(m):
    index = 0
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
        decrypted = effModuloExp(int(i,2),d,n)
        decryptedToBin = decimalToBinary(decrypted)
        decryptedMsg.append(decryptedToBin)
    decryptedMsg[-1] = removePadding(decryptedMsg[-1])
    decryptedString = ""
    for i in decryptedMsg:
        decryptedString += i
    return decryptedString



# 01110101110011010111111000000100
#1011000110101011
print(decrypt(53,143,"011110010000011001001001"))
print(decrypt(53,143,"0011111101011111011100100111001001011001"))
# print(decrypt(7571,45359,"01110101110011010111111000000100"))


