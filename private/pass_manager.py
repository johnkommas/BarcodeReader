#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

from cryptography.fernet import Fernet


def encrypt(password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    token = cipher_suite.encrypt(bytes(password, 'utf-8'))
    return key, token


def decrypt(key, token):
    cipher_suite = Fernet(key)
    password = (cipher_suite.decrypt(token)).decode("utf-8")
    return password
