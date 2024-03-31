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
