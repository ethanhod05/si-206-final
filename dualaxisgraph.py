import requests
import base64
import matplotlib.pyplot as plt
import pandas as pd

# === STEP 1: API Credentials ===
# Spotify
SPOTIFY_CLIENT_ID = "62df1bd7a8b641d899cf46a72d9e8195"
SPOTIFY_CLIENT_SECRET = "98254d2479944fed9ac4c4d2281e8de7"

# Ticketmaster
TICKETMASTER_API_KEY = 'kIOXUHI092ZzeLFH0KGeph5wzKHFd0CV'

# === STEP 2: Helper Functions ===

# Get Spotify Access Token
def get_spotify_token():
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {b64_auth}"},
        data={"grant_type": "client_credentials"}
    )
    return response.json().get('access_token')

# Get Spotify Artist Data
def get_spotify_data(artist_name, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": artist_name, "type": "artist", "limit": 1}
    response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
    items = response.json().get('artists', {}).get('items')
    if items:
        artist = items[0]
        return {
            "followers": artist['followers']['total'],
            "popularity": artist['popularity']
        }
    else:
        return {"followers": 0, "popularity": 0}

# Get Ticketmaster Event Count
def get_ticketmaster_event_count(artist_name):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "keyword": artist_name,
        "countryCode": "US",
        "size": 1
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return 0
    data = response.json()
    return data.get('page', {}).get('totalElements', 0)

# === STEP 3: Artist List ===
artist_names = [
    "Dua Lipa", "J. Cole", "Lana Del Rey", "Stray Kids",
    "Gigi Perez", "Morgan Wallen", "Red Hot Chili Peppers",
    "Megan Moroney", "Jason Aldean", "Creed"
]

# === STEP 4: Collect Data ===
spotify_token = get_spotify_token()
artist_data = []

for artist in artist_names:
    print(f"Fetching data for {artist}...")
    spotify_info = get_spotify_data(artist, spotify_token)
    event_count = get_ticketmaster_event_count(artist)
    artist_data.append({
        "name": artist,
        "followers": spotify_info["followers"],
        "popularity": spotify_info["popularity"],
        "events": event_count
    })

# === STEP 5: Create DataFrame ===
df = pd.DataFrame(artist_data)
df = df.sort_values(by="followers", ascending=False)  # Optional: Sort

# === STEP 6: Plot Dual-Axis Chart ===
fig, ax1 = plt.subplots(figsize=(14, 7))

# Followers bar (left axis)
color = 'tab:blue'
ax1.set_xlabel('Artist', fontsize=12)
ax1.set_ylabel('Spotify Followers', color=color, fontsize=12)
bars = ax1.bar(df['name'], df['followers'], color=color, alpha=0.7)
ax1.tick_params(axis='y', labelcolor=color)
plt.xticks(rotation=45, ha="right")

# Events line (right axis)
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Number of Ticketmaster Events', color=color, fontsize=12)
ax2.plot(df['name'], df['events'], color=color, marker='o', linewidth=2)
ax2.tick_params(axis='y', labelcolor=color)

# Title and Layout
plt.title('Spotify Followers vs Ticketmaster Event Count', fontsize=16)
plt.tight_layout()
plt.grid(axis='y')
plt.show()
