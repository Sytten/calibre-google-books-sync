import string
import random

ASCII_CHARACTER_SET = string.ascii_letters + string.digits


def generate_token(length=43):
    rand = random.SystemRandom()
    return "".join(rand.choice(ASCII_CHARACTER_SET) for _ in range(length))
