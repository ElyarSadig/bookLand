import random


def generate_random_code():
    # Generate a random integer with 6 digits (between 100000 and 999999)
    return str(random.randint(100000, 999999))