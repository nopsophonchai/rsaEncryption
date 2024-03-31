def strToBin(string):
    strToAscii = [ord(char) for char in string]
    AsciiToBin = [bin(asc) for asc in strToAscii]
    ConcatBin = ""
    for i in AsciiToBin:
        ConcatBin += i[2:]
    return ConcatBin
def binary_to_ascii(m):
    partitionedMsg = []
    for i in range(0,len(m),8):
        partitionedMsg.append(m[i:i+8])
    b = []
    for i in partitionedMsg:
        b.append(int(i,2))
    return b
print(binary_to_ascii(decrypt(53,143,"0011111101011111011100100111001001011001")))