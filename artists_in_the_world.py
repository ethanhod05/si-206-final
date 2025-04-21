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
        if len(text) > 1 and len(text) < 50:  #filter to avoid trash
            artists.append(text)

    unique_artists = list(dict.fromkeys(artists))
    return unique_artists


