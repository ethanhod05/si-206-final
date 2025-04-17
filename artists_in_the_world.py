import requests
from bs4 import BeautifulSoup
def get_top_100():
    url = 'https://www.billboard.com/charts/artist-100/'
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    artists = []

  
    for tag in soup.find_all('h3', class_='c-title'):
        text = tag.get_text(strip=True)
        if len(text) > 1 and len(text) < 50:  # crude filter to avoid trash
            artists.append(text)

    unique_artists = list(dict.fromkeys(artists))

#create the integer table for the artists on the list 
#seperate table /// all in the same database



# c.execute('''SELECT name FROM name_id ''')
# name_id = c.fetchall()
#^^^ will give us a list of all the name_ids
    return unique_artists


