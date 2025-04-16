import requests
from bs4 import BeautifulSoup
def get_top_100():
    url = 'https://www.billboard.com/charts/artist-100/'
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Inspect the Billboard page: artist names are inside <h3> with class "c-title"
    artists = []

    # Billboard uses <h3> for artist names, but we need to filter out only the right ones
    for tag in soup.find_all('h3', class_='c-title'):
        text = tag.get_text(strip=True)
        # Billboard artist tags have a length limit and are centered in a pattern
        if len(text) > 1 and len(text) < 50:  # crude filter to avoid trash
            artists.append(text)

    # Remove duplicates (in case it's a chart reused multiple times)
    unique_artists = list(dict.fromkeys(artists))

    # Show top 100
    return unique_artists


