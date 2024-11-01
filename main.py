import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Load data from CSV
df = pd.read_csv('datasets/premier-player-23-24.csv')

# Group by 'age' and 'group' and count occurrences
age_group_counts = df.groupby(['Age', 'Team']).size().unstack(fill_value=0)

# Get unique groups and generate a color map
unique_groups = age_group_counts.columns
colors = cm.get_cmap('tab20', len(unique_groups))  # 'tab20' is a colormap with distinct colors

# Plot the stacked bar chart with generated colors
age_group_counts.plot(kind='barh', stacked=True, figsize=(10, 6), color=[colors(i) for i in range(len(unique_groups))])
plt.title('Count of Each Age by Group')
plt.xlabel('Count')
plt.ylabel('Age')
plt.legend(title='Group')
plt.show()