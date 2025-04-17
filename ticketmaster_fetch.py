# import requests
# from artists_in_the_world import get_top_100
# import json

# TICKETMASTER_API_KEY = "kIOXUHI092ZzeLFH0KGeph5wzKHFd0CV"
# data_list = []


# for artist in get_top_100():    
    
#     params = {
#         "apikey": TICKETMASTER_API_KEY,
#         "keyword": artist,
#         "classificationName": "music",
#         "size": 25,
#         "countryCode": "US"
#     }

#     response = requests.get("https://app.ticketmaster.com/discovery/v2/events.json", params=params)
#     data = response.json()
#     data_list.append(data)

#     if "_embedded" in data and "events" in data["_embedded"]:
#         print("printing out all of the data",data)
#         for event in data["_embedded"]["events"]:
#             name = event["name"]
#             date = event["dates"]["start"].get("localDate", "TBD")
#             url = event["url"]
#             venue = event["_embedded"]["venues"][0]["name"]
#             print(f"{name} at {venue} on {date} — {url}")
#     else:
#         print("No events found.")

# with open('ticketmaster.json', 'w') as file:
#     json.dump(data_list, file, indent=4)
import sqlite3
import requests
from artists_in_the_world import get_top_100

conn = sqlite3.connect("this_one_works.db")
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS UpcomingConcerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name_id TEXT,
    Concerts INTEGER)
''')


try:
    c.execute('''
              SELECT COUNT (Name_id) FROM UpcomingConcerts''')
    
    name = c.fetchone()[0]

except:
    name = 0
    print("name doesnt exist")
# Insert data into table
i = 0
hello = get_top_100()
for i in range(25):
    index = name + i + 3
    artist = hello[index]
    TICKETMASTER_API_KEY = "kIOXUHI092ZzeLFH0KGeph5wzKHFd0CV"
    artist_name = artist

    params = {
        "apikey": TICKETMASTER_API_KEY,
        "keyword": artist_name,
        "classificationName": "music",
        "size": 200,  # Max per page
    }

    response = requests.get("https://app.ticketmaster.com/discovery/v2/events.json", params=params)
    data = response.json()

    if "_embedded" in data and "events" in data["_embedded"]:
        event_count = len(data["_embedded"]["events"])
        print(f"{artist_name} has {event_count} concerts listed.")
        c.execute('''
        INSERT OR IGNORE INTO UpcomingConcerts (Name_id, Concerts)
        VALUES (?, ?)
    ''', (artist_name, event_count))
        conn.commit()
    else:
        event_count = 0
        print("No events found.")
        c.execute('''
        INSERT INTO UpcomingConcerts (Name_id, Concerts)
        VALUES (?, ?)
    ''', (artist_name, event_count))
        conn.commit()

    
