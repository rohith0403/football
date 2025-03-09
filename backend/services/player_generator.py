import numpy as np
from faker import Faker


def generate_name():
    """Generate names for the player"""
    fake_english_name = Faker("en_GB")
    return f"{fake_english_name.first_name_male()} {fake_english_name.last_name_male()}"


def generate_age():
    """Generate Age of the player"""
    mean_age = 26  # Peak of the distribution
    min_age = 17
    max_age = 38
    while True:
        age = np.random.poisson(mean_age)
        if min_age <= age <= max_age:
            return age


def generate_player():
    """Generate Player"""
    name = generate_name()
    age = generate_age()
    return name, age
