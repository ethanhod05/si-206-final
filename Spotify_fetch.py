import requests
import base64

# Replace with your actual Spotify credentials
CLIENT_ID = "62df1bd7a8b641d899cf46a72d9e8195"
CLIENT_SECRET = "98254d2479944fed9ac4c4d2281e8de7"

# Step 1: Get access token
auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
b64_auth = base64.b64encode(auth_str.encode()).decode()

token_response = requests.post(
    "https://accounts.spotify.com/api/token",
    headers={"Authorization": f"Basic {b64_auth}"},
    data={"grant_type": "client_credentials"}
)
access_token = token_response.json().get("access_token")
headers = {"Authorization": f"Bearer {access_token}"}

# List of artists to search
artist_names = ["Drake", "Taylor Swift"]

for artist_name in artist_names:
    print(f"\n=== {artist_name.upper()} ===")

    # Step 2: Search for artist
    search_url = "https://api.spotify.com/v1/search"
    search_params = {"q": artist_name, "type": "artist", "limit": 1}
    search_response = requests.get(search_url, headers=headers, params=search_params)
    results = search_response.json()

    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]
        artist_id = artist["id"]
        followers = artist["followers"]["total"]
        print(f"{artist_name} has {followers:,} followers on Spotify.")

        # Step 3: Get top tracks
        top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        tracks_response = requests.get(top_tracks_url, headers=headers, params={"market": "US"})
        tracks = tracks_response.json()["tracks"]

        print("Top Tracks:")
        for track in tracks:
            print(f"{track['name']} - {track['external_urls']['spotify']}")
    else:
        print(f"No results found for {artist_name}.")
