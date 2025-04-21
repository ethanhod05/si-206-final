import requests
import matplotlib.pyplot as plt
import pandas as pd

API_KEY = 'kIOXUHI092ZzeLFH0KGeph5wzKHFd0CV'

def get_event_locations(artist_name, country_code="US", size=100):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": API_KEY,
        "keyword": artist_name,
        "countryCode": country_code,
        "size": size
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching events for {artist_name}: {response.status_code}")
        return []

    data = response.json()
    events = data.get("_embedded", {}).get("events", [])
    locations = []

    for event in events:
        venues = event.get("_embedded", {}).get("venues", [])
        for venue in venues:
            loc = venue.get("location")
            if loc:
                try:
                    lat = float(loc.get("latitude"))
                    lon = float(loc.get("longitude"))
                    locations.append([lat, lon])
                except:
                    continue
    return locations

def generate_heatmap():
    artist_names = ["Dua Lipa", "J. Cole", "Morgan Wallen", "Red Hot Chili Peppers"]
    all_locations = []

    for artist in artist_names:
        print(f"🎤 Fetching events for {artist}...")
        artist_locations = get_event_locations(artist)
        all_locations.extend(artist_locations)

    if all_locations:
        df = pd.DataFrame(all_locations, columns=["lat", "lon"])
        plt.figure(figsize=(10, 6))
        hb = plt.hexbin(df['lon'], df['lat'], gridsize=30, cmap='plasma', mincnt=1)
        plt.colorbar(hb, label='Event Density')
        plt.title("Ticketmaster Artist Events Heatmap (Static)")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("Visualizations/ticketmaster_event_heatmap.png", dpi=300)
        plt.close()
        print("Map saved as Visualizations/ticketmaster_event_heatmap.png")
    else:
        print("⚠️ No event locations found.")
