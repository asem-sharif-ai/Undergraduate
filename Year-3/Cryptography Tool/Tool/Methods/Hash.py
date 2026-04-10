import hashlib

def generate_hash(text: str, hasher: str='MD5'):
    hasher = {
        'MD5'  : hashlib.md5,
        'SHA3': hashlib.sha3_256
    } [hasher] ()
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()