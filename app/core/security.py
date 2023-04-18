import hashlib

from app.core.config import settings

salt = str.encode(settings.SALT_SECRET_KEY)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    key = hashlib.pbkdf2_hmac("sha256", plain_password.encode('utf-8'), salt, 100000)
    return str(key) == hashed_password


def get_password_hash(password: str) -> str:
    key = hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, 100000)
    return str(key)
