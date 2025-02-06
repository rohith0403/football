""" Player Initializer Module """

import random
import time

import numpy as np
from faker import Faker

from classes.Player import Player
from models.models import GK, Attributes, Intrinsic, Mental, Physical, Technical

fake = Faker()


def generate_name_and_nationality():
    """Generate names for the player"""
    # Create Faker instances for Brazilian Portuguese and Norwegian locales
    fake_english = Faker("en_GB")
    # Generate Brazilian names
    return [fake_english.name_male(), ["England"]]


def generate_age():
    """Generate Age of the player"""
    mean_age = 26  # Peak of the distribution
    min_age = 18
    max_age = 34
    while True:
        age = np.random.poisson(mean_age)
        if min_age <= age <= max_age:
            return age


def generate_techincal_attributes(range1, range2):
    """Generate Technical Attributes"""
    while True:
        numbers = [random.randint(1, 20) for _ in range(11)]
        total = sum(numbers)
        if range1 <= total <= range2:
            break
    technical_attributes = Technical(
        Crossing=numbers[0],
        Dribbling=numbers[1],
        Finishing=numbers[2],
        FirstTouch=numbers[3],
        FreeKickTaking=numbers[4],
        Heading=numbers[5],
        Long_Shots=numbers[6],
        Long_Throws=numbers[7],
        Marking=numbers[8],
        Passing=numbers[9],
        Tackling=numbers[10],
    )
    return technical_attributes


def generate_mental_attributes(range1, range2):
    """Generate Mental attributes"""
    while True:
        numbers = [random.randint(1, 20) for _ in range(12)]
        total = sum(numbers)
        if range1 <= total <= range2:
            break
    mental_attributes = Mental(
        Aggression=numbers[0],
        Bravery=numbers[1],
        Composure=numbers[2],
        Concentration=numbers[3],
        Decisions=numbers[4],
        Determination=numbers[5],
        Flair=numbers[6],
        Leadership=numbers[7],
        Positioning=numbers[8],
        Teamwork=numbers[9],
        Vision=numbers[10],
        WorkRate=numbers[11],
    )
    return mental_attributes


def generate_physical_attributes(range1, range2):
    """Generate Physical attributes"""
    while True:
        numbers = [random.randint(1, 20) for _ in range(4)]
        total = sum(numbers)
        if range1 <= total <= range2:
            break
    physical_attributes = Physical(
        Strength=numbers[0],
        NaturalFitness=numbers[1],
        Pace=numbers[2],
        Stamina=numbers[3],
    )
    return physical_attributes


def generate_gk_attributes(range1, range2):
    """Generate GK attributes"""
    while True:
        numbers = [random.randint(1, 20) for _ in range(5)]
        total = sum(numbers)
        # if 33 <= total <= 66:
        if range1 <= total <= range2:
            break
    gk_attribtues = GK(
        GKDiving=numbers[0],
        GKHandling=numbers[1],
        GKKicking=numbers[2],
        GKPositioning=numbers[3],
        GKReflexes=numbers[4],
    )
    return gk_attribtues


def generate_intrinsic_attributes(range1, range2):
    """Generate Intrinsic attributes"""
    while True:
        numbers = [random.randint(1, 20) for _ in range(6)]
        total = sum(numbers)
        # if 54 <= total <= 106:
        if range1 <= total <= range2:
            break
    intrinsic_attributes = Intrinsic(
        Confidence=numbers[0],
        Consistency=numbers[1],
        Proffesionalism=numbers[2],
        BigGamePlayer=numbers[3],
        Loyalty=numbers[4],
        Ambition=numbers[5],
    )
    return intrinsic_attributes


def generate_attributes():
    """Generates Attributes"""
    # Player is a Goalkeeper
    if random.randint(0, 11) % 11 == 0:
        technical_attributes = generate_techincal_attributes(1, 144)
        mental_attributes = generate_mental_attributes(1, 144)
        physical_attributes = generate_physical_attributes(1, 54)
        gk_attributes = generate_gk_attributes(30, 90)
        intrinsic_attributes = generate_intrinsic_attributes(40, 106)
        attributes = Attributes(
            technical=technical_attributes,
            mental=mental_attributes,
            physical=physical_attributes,
            gk=gk_attributes,
            intrinsic=intrinsic_attributes,
        )
    else:
        technical_attributes = generate_techincal_attributes(60, 200)
        mental_attributes = generate_mental_attributes(60, 250)
        physical_attributes = generate_physical_attributes(40, 144)
        gk_attributes = generate_gk_attributes(1, 25)
        intrinsic_attributes = generate_intrinsic_attributes(40, 144)
        attributes = Attributes(
            technical=technical_attributes,
            mental=mental_attributes,
            physical=physical_attributes,
            gk=gk_attributes,
            intrinsic=intrinsic_attributes,
        )
    return attributes


def generate_player(team=""):
    """Method to generate player"""
    name, nationality = generate_name_and_nationality()
    age = generate_age()
    attributes = generate_attributes()
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    random_part = random.randint(0, 999999)
    serial_id = f"#{timestamp:013d}{random_part:06d}"
    player = Player(serial_id, name, age, nationality, attributes, team=team)
    return player
