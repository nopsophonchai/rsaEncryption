from math import log2, floor, ceil
import sympy
import random

# Utility functions
def OneAndZeroes(block_size, num_len):
    padding_needed = block_size - num_len
    return "1" + "0" * (padding_needed - 1)

def decimalToBinary(m, bits=None):
    binary = bin(m)[2:]
    if bits:
        return binary.zfill(bits)
    return binary

def stringToBinary(m):
    return ''.join(format(ord(char), '08b') for char in m)

def binaryToString(binary):
    n = 8
    binary_chunks = [binary[i:i + n] for i in range(0, len(binary), n)]
    ascii_values = [int(chunk, 2) for chunk in binary_chunks]
    chars = [chr(ascii_val) for ascii_val in ascii_values]
    return ''.join(chars)

def detectBin(m):
    return all(c in '01' for c in m)

def removePadding(m):
    index = 0
    if m[-1] == '1':
        return m
    for i in range(1, len(m)):
        if m[-i] == "1":
            index = -i
            break
    return m[:index]

def effModuloExp(base, exp, mod):
    base = int(base, 2)  # Convert the binary string to an integer
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

# RSA encryption function
def encrypt(e, n, m):
    blockSize = floor(log2(n))
    binMsg = m if detectBin(m) else stringToBinary(m)
    print(f"Binary message: {binMsg}")

    partitionedMsg = []
    for i in range(0, len(binMsg), blockSize):
        block = binMsg[i:i + blockSize]
        if len(block) < blockSize:
            block += OneAndZeroes(blockSize, len(block))
        partitionedMsg.append(block)
    print(f"Partitioned message: {partitionedMsg}")

    encryptedMsg = []
    newBlockSize = ceil(log2(n))
    for part in partitionedMsg:
        encrypted = effModuloExp(part, e, n)
        encryptedToBin = decimalToBinary(encrypted, newBlockSize)
        encryptedMsg.append(encryptedToBin)
    encryptedString = ''.join(encryptedMsg)
    return encryptedString

# RSA decryption function
def decrypt(d, n, m):
    blockSize = ceil(log2(n))
    newBlockSize = floor(log2(n))
    binMsg = m
    partitionedMsg = [binMsg[i:i + blockSize] for i in range(0, len(binMsg), blockSize)]
    print(f"Partitioned encrypted message: {partitionedMsg}")

    decryptedMsg = []
    for part in partitionedMsg:
        decrypted = effModuloExp(part, d, n)
        decryptedToBin = decimalToBinary(decrypted, newBlockSize)
        decryptedMsg.append(decryptedToBin)
    print(f"Decrypted binary message: {decryptedMsg}")

    decryptedMsg[-1] = removePadding(decryptedMsg[-1])
    decryptedString = ''.join(decryptedMsg)
    print(f"Decrypted string: {decryptedString}")
    return binaryToString(decryptedString)

# Example usage
public_key = (257759, 144115)
private_key = (257759, 237691)

# Encrypt and decrypt a message
message = "Hello"
print(f"Original message: {message}")

encrypted_message = encrypt(public_key[1], public_key[0], message)
print(f"Encrypted message: {encrypted_message}")

decrypted_message = decrypt(private_key[1], private_key[0], encrypted_message)
print(f"Decrypted message: {decrypted_message}")
