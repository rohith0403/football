import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# from generators.player_generator import generate_pool
# import csv

# player_pool = generate_pool()

# for player in player_pool:
#     with open('player_pool.csv', 'w',) as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['Name', 'Role', 'Overall Ability', 'Shooting', 'Passing', 'Dribbling', 'Defending'])
#         for player in player_pool:
#             writer.writerow([player.name, player.role, player.current_ability, player.shooting, player.passing, player.dribbling, player.defending])

# Load data from CSV
df = pd.read_csv('player_pool.csv')
value_counts = df['Role'].value_counts()
print(value_counts)