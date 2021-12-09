import hashlib


def password_hash(user_password):
    return hashlib.md5(user_password.encode('utf-8')).hexdigest()

