import hashlib
import string
import random


def generate_random_string(length: int):
    letters = string.ascii_letters + string.digits + string.punctuation

    return "".join(random.choice(letters) for _ in range(0, length))


def generate_random_up_letters(length: int):
    return "".join(random.choice(string.ascii_uppercase) for _ in range(0, length))


def generate_random_low_letters(length: int):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(0, length))


def generate_token(length: int):
    return '-'.join([generate_random_up_letters(4) for _ in range(length)])


def md5_string(s: str):
    return hashlib.md5(s.encode("utf-8")).hexdigest()
