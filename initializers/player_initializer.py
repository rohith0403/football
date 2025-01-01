import random
import time

import numpy as np
from faker import Faker

from classes.Player import Player

# from db.store import insert_into_player_pool
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
        numbers = [random.randint(1, 20) for _ in range(14)]
        total = sum(numbers)
        # if 98 <= total <= 196:
        if range1 <= total <= range2:
            break
    technical_attributes = Technical(
        Corners=numbers[0],
        Crossing=numbers[1],
        Dribbling=numbers[2],
        Finishing=numbers[3],
        FirstTouch=numbers[4],
        FreeKickTaking=numbers[5],
        Heading=numbers[6],
        Long_Shots=numbers[7],
        Long_Throws=numbers[8],
        Marking=numbers[9],
        Passing=numbers[10],
        Penalty_Taking=numbers[11],
        Tackling=numbers[12],
        Technique=numbers[13],
    )
    return technical_attributes


def generate_mental_attributes(range1, range2):
    """Generate Mental attributes"""
    while True:
        numbers = [random.randint(1, 20) for _ in range(14)]
        total = sum(numbers)
        # if 98 <= total <= 196:
        if range1 <= total <= range2:
            break
    mental_attributes = Mental(
        Aggression=numbers[0],
        Anticipation=numbers[1],
        Bravery=numbers[2],
        Composure=numbers[3],
        Concentration=numbers[4],
        Decisions=numbers[5],
        Determination=numbers[6],
        Flair=numbers[7],
        Leadership=numbers[8],
        OffTheBall=numbers[9],
        Positioning=numbers[10],
        Teamwork=numbers[11],
        Vision=numbers[12],
        WorkRate=numbers[13],
    )
    return mental_attributes


def generate_physical_attributes(range1, range2):
    """Generate Physical attributes"""
    while True:
        numbers = [random.randint(1, 20) for _ in range(8)]
        total = sum(numbers)
        # if 54 <= total <= 106:
        if range1 <= total <= range2:
            break
    physical_attributes = Physical(
        Strength=numbers[0],
        Acceleration=numbers[1],
        Agility=numbers[2],
        Balance=numbers[3],
        JumpingReach=numbers[4],
        NaturalFitness=numbers[5],
        Pace=numbers[6],
        Stamina=numbers[7],
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
        numbers = [random.randint(1, 20) for _ in range(8)]
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
        Versatility=numbers[5],
        CareerAmbition=numbers[6],
        MoneyAmbition=numbers[7],
    )
    return intrinsic_attributes


def generate_attributes():
    """Generates Attributes"""
    # Player is a Goalkeeper
    if random.randint(0, 11) % 11 == 0:
        technical_attributes = generate_techincal_attributes(1, 98)
        mental_attributes = generate_mental_attributes(1, 196)
        physical_attributes = generate_physical_attributes(1, 54)
        gk_attributes = generate_gk_attributes(44, 72)
        intrinsic_attributes = generate_intrinsic_attributes(54, 106)
        attributes = Attributes(
            technical=technical_attributes,
            mental=mental_attributes,
            physical=physical_attributes,
            gk=gk_attributes,
            intrinsic=intrinsic_attributes,
        )
    else:
        technical_attributes = generate_techincal_attributes(98, 196)
        mental_attributes = generate_mental_attributes(98, 196)
        physical_attributes = generate_physical_attributes(54, 106)
        gk_attributes = generate_gk_attributes(1, 25)
        intrinsic_attributes = generate_intrinsic_attributes(54, 106)
        attributes = Attributes(
            technical=technical_attributes,
            mental=mental_attributes,
            physical=physical_attributes,
            gk=gk_attributes,
            intrinsic=intrinsic_attributes,
        )
    return attributes


def generate_player():
    """Method to generate player"""
    name, nationality = generate_name_and_nationality()
    age = generate_age()
    attributes = generate_attributes()
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    random_part = random.randint(0, 999999)
    serial_id = f"#{timestamp:013d}{random_part:06d}"
    player = Player(
        serial_id, name, age, nationality, random.randint(50, 200), attributes
    )
    return player


def add_players_to_pool():
    """Add player to DB"""
    for i in range(2000):
        player = generate_player()
        insert_into_player_pool(player)
