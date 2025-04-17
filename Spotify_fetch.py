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

#  Step 2: Fetch top artists data 
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

# Step 3: Save to JSON file
with open('data.json', 'w') as file:
    json.dump(data_list, file, indent=4)

# Save to SQLite database 
conn = sqlite3.connect("this_one_works.db")
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS SpotifyArtists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    followers INTEGER,
    popularity INTEGER
)
''')
#print("here\n")
#print(data_list)
try:
    c.execute('''
              SELECT COUNT (id) FROM SpotifyArtists''')
    
    name = c.fetchone()[0]

except:
    name = 0
    print("name doesnt exist")
# Insert data into table
i = 0

for i in range(25):
    index = name + i
    artist = data_list[index]
    c.execute('''
        INSERT INTO SpotifyArtists (name, followers, popularity)
        VALUES (?, ?, ?)
    ''', (artist['name'], artist['followers'], artist['popularity']))

conn.commit()
conn.close()

# Playlist Artist Utility 
def get_artists_from_playlist(access_token, playlist_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    params = {"limit": 100} #i can change this to 25 to fit our goal
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
    print(type(unique_artists))
    return unique_artists