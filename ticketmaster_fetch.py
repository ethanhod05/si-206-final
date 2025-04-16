import requests
from artists_in_the_world import get_top_100
import json

TICKETMASTER_API_KEY = "kIOXUHI092ZzeLFH0KGeph5wzKHFd0CV"
data_list = []


for artist in get_top_100():    
    
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "keyword": artist,
        "classificationName": "music",
        "size": 25,
        "countryCode": "US"
    }

    response = requests.get("https://app.ticketmaster.com/discovery/v2/events.json", params=params)
    data = response.json()
    data_list.append(data)

    if "_embedded" in data and "events" in data["_embedded"]:
        print("printing out all of the data",data)
        for event in data["_embedded"]["events"]:
            name = event["name"]
            date = event["dates"]["start"].get("localDate", "TBD")
            url = event["url"]
            venue = event["_embedded"]["venues"][0]["name"]
            print(f"{name} at {venue} on {date} — {url}")
    else:
        print("No events found.")

with open('ticketmaster.json', 'w') as file:
    json.dump(data_list, file, indent=4)