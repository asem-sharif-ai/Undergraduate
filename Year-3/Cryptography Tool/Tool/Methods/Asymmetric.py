from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def encode(base_64_str):
    return base64.b64decode(base_64_str)

def decode(base_64_obj):
    return base64.b64encode(base_64_obj).decode('utf-8')

def format_keys(keys:tuple) -> tuple[str, str]:    
    public_body = "\n".join(
        line for line in keys[0].export_key().decode('utf-8').splitlines() if not line.startswith('-----')
    )
    private_body = '\n'.join(
        line for line in keys[1].export_key().decode('utf-8').splitlines() if not line.startswith('-----')
    )
    return public_body, private_body

def setup_keys(keys:tuple):
    return RSA.import_key(keys[0]), RSA.import_key(keys[1])

def generate_keys(key_size:int=2048):
    key = RSA.generate(key_size)
    return key.publickey(), key

def generate_cipher(key):
    return PKCS1_OAEP.new(key)

def encrypt(public_key, plaintext:str) -> str:
    cipher = generate_cipher(public_key)
    ciphertext = cipher.encrypt(plaintext.encode('utf-8'))
    return decode(ciphertext)

def decrypt(private_key, ciphertext:str) -> str:
    cipher = generate_cipher(private_key)
    decrypted = cipher.decrypt(encode(ciphertext))
    return decrypted.decode('utf-8')