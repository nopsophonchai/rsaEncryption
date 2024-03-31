from math import log2,floor,ceil
def OneAndZeroes(blockSize, numLen):
    paddingNeeded = blockSize - numLen
    zeroes = "0" * (paddingNeeded - 1)
    padding = "1" + zeroes
    return padding


def decimalToBinary(m):
    return "{0:b}".format(int(m))

def effModuloExp(a,m,n):
    bits = decimalToBinary(m)
    d = 1
    for bi in bits:
        d = d*d %n
        if bi != "0":
            d = (d*a) % n 
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
# padding = OneAndZeroes(7,3)
# print(padding)
# print(effModuloExp(88,77,143))
# ConcatBin = strToBin("hello")
# print(ConcatBin)

