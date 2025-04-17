import requests
import base64
import json
import sqlite3
from artists_in_the_world import get_top_100

# Spotify Credentials 
CLIENT_ID = "62df1bd7a8b641d899cf46a72d9e8195"
CLIENT_SECRET = "98254d2479944fed9ac4c4d2281e8de7"

# Get access token
auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
b64_auth = base64.b64encode(auth_str.encode()).decode()

token_response = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={"Authorization": f"Basic {b64_auth}"},
    data={"grant_type": "client_credentials"}
)
access_token = token_response.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

# Fetch top artists data 
artist_names = get_top_100()
data_list = []

for artist_name in artist_names:
    print(f"\n=== {artist_name.upper()} ===")

    search_url = "https://api.spotify.com/v1/search"
    search_params = {"q": artist_name, "type": "artist", "limit": 1}
    search_response = requests.get(search_url, headers=headers, params=search_params)
    results = search_response.json()

    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]
        name = artist["name"]
        popularity = artist["popularity"]
        followers = artist["followers"]["total"]
        artist_id = artist["id"]

        print(f"Name: {name}")
        print(f"Popularity: {popularity}")
        print(f"Followers: {followers:,}")

        data_list.append({
            "name": name,
            "popularity": popularity,
            "followers": followers,
            "id": artist_id
        })
    else:
        print(f"No results found for {artist_name}.")

# Save to JSON file
with open('data.json', 'w') as file:
    json.dump(data_list, file, indent=4)

# Save to SQLite database 
conn = sqlite3.connect("this_one_works.db")
c = conn.cursor()

# Create PopularityLevel table
c.execute('''
CREATE TABLE IF NOT EXISTS PopularityLevel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level TEXT
)
''')

# Insert levels if not already present
c.execute("SELECT COUNT(*) FROM PopularityLevel")
if c.fetchone()[0] == 0:
    c.executemany("INSERT INTO PopularityLevel (level) VALUES (?)", [
        ('Low',), ('Mid',), ('High',)
    ])

# Create SpotifyArtists table (with popularity_level_id FK)
c.execute('''
CREATE TABLE IF NOT EXISTS SpotifyArtists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    followers INTEGER,
    popularity INTEGER
)
''')

# Add popularity_level_id column if not already present
try:
    c.execute("ALTER TABLE SpotifyArtists ADD COLUMN popularity_level_id INTEGER REFERENCES PopularityLevel(id)")
except sqlite3.OperationalError:
    pass  # Column already exists

# Check how many entries already exist
try:
    c.execute("SELECT COUNT(id) FROM SpotifyArtists")
    existing_count = c.fetchone()[0]
except:
    existing_count = 0

# Classify popularity level
def get_popularity_level_id(score):
    if score < 85:
        return 1  # Low
    elif score < 93:
        return 2  # Mid
    else:
        return 3  # High

# Insert next 25 artists
for i in range(25):
    index = existing_count + i
    artist = data_list[index]
    popularity_level_id = get_popularity_level_id(artist["popularity"])
    c.execute('''
        INSERT INTO SpotifyArtists (name, followers, popularity, popularity_level_id)
        VALUES (?, ?, ?, ?)
    ''', (artist['name'], artist['followers'], artist['popularity'], popularity_level_id))

conn.commit()
conn.close()

# Playlist Artist Utility 
def get_artists_from_playlist(access_token, playlist_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    params = {"limit": 100}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error fetching playlist:", response.status_code, response.text)
        return []

    data = response.json()
    artist_names = []

    for item in data.get("items", []):
        track = item.get("track")
        if track and track.get("artists"):
            for artist in track["artists"]:
                artist_names.append(artist["name"])

    # Remove duplicates while preserving order
    seen = set()
    unique_artists = [name for name in artist_names if not (name in seen or seen.add(name))]
    return unique_artists
