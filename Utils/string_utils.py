import string
import random


def rand_string(length):
    return "".join(
        random.choice(
            string.ascii_letters + string.digits + string.punctuation
        )
        for _ in range(0, length)
    )
