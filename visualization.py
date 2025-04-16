import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.linear_model import LinearRegression

# Spotify artist data
artists = [
    {"name": "Nate Smith", "popularity": 72, "followers": 491759},
    {"name": "Gigi Perez", "popularity": 80, "followers": 1093491},
    {"name": "Alice In Chains", "popularity": 77, "followers": 5751845},
    {"name": "Megan Moroney", "popularity": 77, "followers": 797189},
    {"name": "Red Hot Chili Peppers", "popularity": 85, "followers": 22365071},
    {"name": "Tommy Richman", "popularity": 75, "followers": 876632},
    {"name": "Jason Aldean", "popularity": 77, "followers": 6833763},
    {"name": "Stray Kids", "popularity": 86, "followers": 18779688},
    {"name": "Dua Lipa", "popularity": 89, "followers": 45845968},
    {"name": "Blake Shelton", "popularity": 74, "followers": 7421490},
    {"name": "Creed", "popularity": 77, "followers": 3909302},
    {"name": "PARTYNEXTDOOR", "popularity": 88, "followers": 8839109},
    {"name": "Led Zeppelin", "popularity": 79, "followers": 15391805},
    {"name": "J. Cole", "popularity": 86, "followers": 26112786},
    {"name": "JENNIE", "popularity": 89, "followers": 9834739},
    {"name": "Dasha", "popularity": 72, "followers": 330809},
    {"name": "Lana Del Rey", "popularity": 92, "followers": 46576145},
    {"name": "Journey", "popularity": 77, "followers": 6130899},
    {"name": "Lainey Wilson", "popularity": 77, "followers": 1221619}
]

# Create DataFrame
df = pd.DataFrame(artists)
df['log_followers'] = np.log10(df['followers'])

# Fit linear regression model
X = df[['log_followers']]
y = df['popularity']
reg = LinearRegression().fit(X, y)
df['predicted'] = reg.predict(X)
df['residual'] = df['popularity'] - df['predicted']

# Set color based on performance
df['performance'] = df['residual'].apply(lambda x: 'Overperforming' if x > 3 else ('Underperforming' if x < -3 else 'On-Trend'))

# Plot
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='log_followers', y='popularity', hue='performance', palette={'Overperforming': 'green', 'Underperforming': 'red', 'On-Trend': 'gray'}, s=100)
sns.lineplot(x=df['log_followers'], y=df['predicted'], color='blue', label='Trendline')

# Add annotations for some key artists
for _, row in df.iterrows():
    if abs(row['residual']) > 4:
        plt.text(row['log_followers']+0.01, row['popularity']+0.5, row['name'], fontsize=9)

plt.title("Spotify Artists: Popularity vs Followers (Log Scale)", fontsize=16)
plt.xlabel("Log10(Followers)", fontsize=12)
plt.ylabel("Popularity", fontsize=12)
plt.legend(title="Performance")
plt.grid(True)
plt.tight_layout()
plt.show()
