from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
import base64

def encode(base_64_str):
    return base64.b64decode(base_64_str)

def decode(base_64_obj):
    return base64.b64encode(base_64_obj).decode('utf-8')

def generate_key(key_length:int):
    return get_random_bytes(key_length)

def generate_iv(algorithm:str):
    return get_random_bytes(16 if algorithm == 'AES' else 8)

def generate_cipher(algorithm:str, mode:str, key:bytes, iv:bytes):
    return {'AES': AES, 'DES': DES}[algorithm].new(
        key,
        {'CBC': AES.MODE_CBC, 'CFB': AES.MODE_CFB, 'OFB': AES.MODE_OFB}[mode],
        iv
    )

def encrypt(algorithm:str, mode:str, key:bytes, iv:bytes, plaintext:str) -> str:
    cipher = generate_cipher(algorithm, mode, key, iv)
    plaintext_bytes = plaintext.encode('utf-8')

    if mode == 'CBC':
        block_size = cipher.block_size
        padding = block_size - len(plaintext_bytes) % block_size
        plaintext_bytes += bytes([padding]) * padding

    ciphertext = cipher.encrypt(plaintext_bytes)
    return base64.b64encode(ciphertext).decode('utf-8')

def decrypt(algorithm:str, mode:str, key:bytes, iv:bytes, ciphertext:str) -> str:
    cipher = generate_cipher(algorithm, mode, key, iv)
    ciphertext_bytes = base64.b64decode(ciphertext)
    plaintext_bytes = cipher.decrypt(ciphertext_bytes)

    if mode == 'CBC':
        padding = plaintext_bytes[-1]
        plaintext_bytes = plaintext_bytes[:-padding]

    return plaintext_bytes.decode('utf-8')