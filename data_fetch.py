import requests
import base64
import sqlite3

# SPOTIFY & TICKETMASTER API credentials (you must replace these)
SPOTIFY_CLIENT_ID = "62df1bd7a8b641d899cf46a72d9e8195"
SPOTIFY_CLIENT_SECRET = "98254d2479944fed9ac4c4d2281e8de7"
TICKETMASTER_API_KEY = "kIOXUHI092ZzeLFH0KGeph5wzKHFd0CV"

ARTIST_NAME = "Taylor Swift"
DB_NAME = "music_data.db"

def setup_db():
    """
    Initializes the SQLite database with normalized structure:
    - Artists table for shared reference
    - SpotifyStats for top track data
    - TicketmasterEvents for concert data
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Artists (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)')
    cur.execute('''CREATE TABLE IF NOT EXISTS SpotifyStats (
        artist_id INTEGER,
        track_name TEXT,
        popularity INTEGER,
        FOREIGN KEY (artist_id) REFERENCES Artists(id)
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS TicketmasterEvents (
        id TEXT PRIMARY KEY,
        artist_id INTEGER,
        event_name TEXT,
        date TEXT,
        venue TEXT,
        FOREIGN KEY (artist_id) REFERENCES Artists(id)
    )''')
    conn.commit()
    conn.close()

def get_spotify_token():
    """
    Authenticates with the Spotify Web API using Client Credentials Flow
    Reference: https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow
    """
    auth_str = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {b64_auth}"},
        data={"grant_type": "client_credentials"}
    )
    return response.json().get("access_token")

def fetch_spotify_data(token, artist_name):
    """
    Fetches artist ID and top tracks from Spotify Web API.
    Endpoints used:
    - Search Artist: https://api.spotify.com/v1/search
    - Get Top Tracks: https://api.spotify.com/v1/artists/{id}/top-tracks
    """
    headers = {"Authorization": f"Bearer {token}"}
    
    # Search for artist by name
    search = requests.get("https://api.spotify.com/v1/search", headers=headers,
                          params={"q": artist_name, "type": "artist", "limit": 1})
    # artist = search.json()["artists"]["items"][0]
    artist = search.json()
    print("here", artist["artists"])
    # artist_id = artist["id"]

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Store artist in central Artists table
    cur.execute("INSERT OR IGNORE INTO Artists (name) VALUES (?)", (artist_name,))
    cur.execute("SELECT id FROM Artists WHERE name = ?", (artist_name,))
    db_artist_id = cur.fetchone()[0]

    # Get top tracks from Spotify
    tracks = requests.get(f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
                          headers=headers, params={"market": "US"}).json()["tracks"]

    for track in tracks[:10]:  # LIMIT to 10 tracks per run to meet rubric
        cur.execute('''INSERT OR IGNORE INTO SpotifyStats VALUES (?, ?, ?)''',
                    (db_artist_id, track['name'], track['popularity']))

    conn.commit()
    conn.close()

def fetch_ticketmaster_data(artist_name):
    """
    Fetches event data from Ticketmaster Discovery API
    Reference: https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
    """
    response = requests.get("https://app.ticketmaster.com/discovery/v2/events.json", params={
        "apikey": TICKETMASTER_API_KEY,
        "keyword": artist_name,
        "classificationName": "music",
        "countryCode": "US",
        "size": 10  # LIMIT to 10 events per run
    })
    data = response.json()

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO Artists (name) VALUES (?)", (artist_name,))
    cur.execute("SELECT id FROM Artists WHERE name = ?", (artist_name,))
    db_artist_id = cur.fetchone()[0]

    if "_embedded" in data and "events" in data["_embedded"]:
        for event in data["_embedded"]["events"]:
            try:
                cur.execute('''INSERT OR IGNORE INTO TicketmasterEvents VALUES (?, ?, ?, ?, ?)''', (
                    event["id"],
                    db_artist_id,
                    event["name"],
                    event["dates"]["start"].get("localDate", "TBD"),
                    event["_embedded"]["venues"][0]["name"]
                ))
            except Exception:
                continue

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_db()
    token = get_spotify_token()
    fetch_spotify_data(token, ARTIST_NAME)
    fetch_ticketmaster_data(ARTIST_NAME)
