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
