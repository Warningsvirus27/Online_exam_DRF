from cryptography.fernet import Fernet


def make_key():
    return Fernet.generate_key()


def generate_password(key, password):
    f = Fernet(key)
    token = f.encrypt(bytes(password, 'UTF-8'))
    return token
