from faker import Faker
from models.Player import Player
import random
from models.Club import Man_City, Arsenal, Liverpool, Chelsea, Man_United, Spurs

# # Create Faker instances for Brazilian Portuguese and Norwegian locales
# fake_brazil = Faker("pt_BR")
# fake_norway = Faker("no_NO")
# # Generate Brazilian names
# print("Brazilian name:", fake_brazil.name_male())
# # Generate Norwegian names
# print("Norwegian name:", fake_norway.name_male())

fake = Faker()
ROLES = ("Defender", "Midfielder", "Attacker")
TEAMS = (Man_City, Arsenal, Liverpool, Chelsea, Man_United, Spurs)


def generate_ability():
    number = 0
    for _ in range(20):
        if random.random() <= 0.01:  # 1% chance
            # Generate a number outside the 20-40 range
            number = (
                random.choice(range(15, 20))
                if random.random() < 0.5
                else random.choice(range(40, 45))
            )
        else:
            # Generate a number within the 20-40 range
            number = random.randint(20, 40)
    return number


def generate_pool():
    global ROLES
    player_pool = []
    for i in range(30):
        role = ROLES[random.randint(0, 2)]
        ability = generate_ability()
        name = fake.name_male()
        new_player = Player(name, role, ability, TEAMS[i % 6])
        TEAMS[i % 6].pick_player(new_player)
    return player_pool
