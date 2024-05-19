from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64

key = os.urandom(32)

def encrypt_message(message,key):
    
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()

    return base64.b64encode(iv + encrypted_message).decode('utf-8')

def decrypt_message(encrypted_message,key):
    encrypted_message = base64.b64decode(encrypted_message)
  
    iv = encrypted_message[:16]
    encrypted_message= encrypted_message[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    decryptor = cipher.decryptor()

    decrypted_padded_message = decryptor.update(encrypted_message) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()

    return decrypted_message.decode('utf-8')

# print(encrypt_message('Hello',int(111111).to_bytes(16, byteorder='big')))
print(decrypt_message('nh+Ibd+E9Q6JE5N+LZnr7aEMFTn3tTwW/KF78yVqaTE=',int(111111).to_bytes(16, byteorder='big')))
