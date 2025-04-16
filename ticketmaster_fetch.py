import requests

TICKETMASTER_API_KEY = "kIOXUHI092ZzeLFH0KGeph5wzKHFd0CV"
artist_name = "Taylor Swift"

params = {
    "apikey": TICKETMASTER_API_KEY,
    "keyword": artist_name,
    "classificationName": "music",
    "size": 10,
    "countryCode": "US"
}

response = requests.get("https://app.ticketmaster.com/discovery/v2/events.json", params=params)
data = response.json()

if "_embedded" in data and "events" in data["_embedded"]:
    for event in data["_embedded"]["events"]:
        name = event["name"]
        date = event["dates"]["start"].get("localDate", "TBD")
        url = event["url"]
        venue = event["_embedded"]["venues"][0]["name"]
        print(f"{name} at {venue} on {date} — {url}")
else:
    print("No events found.")
