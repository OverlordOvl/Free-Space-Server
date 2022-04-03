import hashlib
import re
import string as str_util
import random


def generate_random_string(length: int):
    letters = str_util.ascii_letters + str_util.digits + str_util.punctuation

    return "".join(random.choice(letters) for _ in range(0, length))


def generate_random_up_letters(length: int):
    return "".join(
        random.choice(str_util.ascii_uppercase) for _ in range(0, length)
    )


def generate_random_low_letters(length: int):
    return "".join(
        random.choice(str_util.ascii_lowercase) for _ in range(0, length)
    )


def generate_token(length: int):
    return "-".join([generate_random_up_letters(4) for _ in range(length)])


def md5_string(s: str):
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def snake_to_camel(string: str):
    return "".join(word.title() for word in string.split("_"))


def camel_to_snake(string: str):
    string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", string).lower()
