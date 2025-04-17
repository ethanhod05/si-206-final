import requests
import base64
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

# === Spotify API credentials ===
SPOTIFY_CLIENT_ID = "62df1bd7a8b641d899cf46a72d9e8195"
SPOTIFY_CLIENT_SECRET = "98254d2479944fed9ac4c4d2281e8de7"

# === Step 1: Get Spotify access token ===
def get_spotify_token():
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {b64_auth}"},
        data={"grant_type": "client_credentials"}
    )
    return response.json().get("access_token")

# === Step 2: Get artist data ===
def get_artist_data(artist_name, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": artist_name, "type": "artist", "limit": 1}
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    items = response.json().get('artists', {}).get('items')
    if items:
        artist = items[0]
        return {
            "name": artist['name'],
            "popularity": artist['popularity'],
            "followers": artist['followers']['total']
        }

# === Step 3: Define artist list ===
artist_names = [
    "Dua Lipa", "J. Cole", "Lana Del Rey", "Stray Kids",
    "Gigi Perez", "Morgan Wallen", "Red Hot Chili Peppers",
    "Megan Moroney", "Jason Aldean", "Creed"
]

# === Step 4: Collect data ===
token = get_spotify_token()
artist_data = []

for name in artist_names:
    print(f"Fetching data for {name}...")
    result = get_artist_data(name, token)
    if result:
        artist_data.append(result)

# === Step 5: Create DataFrame and plot ===
df = pd.DataFrame(artist_data)
df['size'] = np.sqrt(df['followers']) / 100  # scale for bubble size

plt.figure(figsize=(12, 8))
plt.scatter(
    df['popularity'], df['followers'],
    s=df['size'] * 100, alpha=0.6,
    color='skyblue', edgecolors='black'
)

# Add text labels
for _, row in df.iterrows():
    plt.text(row['popularity'] + 0.3, row['followers'], row['name'], fontsize=9)

# Titles and axis labels
plt.title("Spotify Artist Popularity vs Followers (Live Data)", fontsize=16)
plt.xlabel("Spotify Popularity (0–100)", fontsize=12)
plt.ylabel("Spotify Followers", fontsize=12)
plt.yscale('log')

# Format Y-axis with M/K labels
ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(
    lambda x, _: f'{int(x/1e6)}M' if x >= 1e6 else f'{int(x/1e3)}K'))

plt.grid(True)
plt.tight_layout()
plt.show()
