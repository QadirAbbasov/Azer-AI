from cryptography.fernet import Fernet
import os

KEY_FILE = 'secret.key'

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()

def encrypt_data(data: str) -> bytes:
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode('utf-8'))

def decrypt_data(token: bytes) -> str:
    key = load_key()
    f = Fernet(key)
    return f.decrypt(token).decode('utf-8') 