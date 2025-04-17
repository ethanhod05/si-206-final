def generate_visualization():
    from matplotlib import pyplot as plt
    import requests
    import base64
    import json
    import sqlite3
    import pandas as pd
    import numpy as np
    import seaborn as sns
    from sklearn.linear_model import LinearRegression

    CLIENT_ID = "62df1bd7a8b641d899cf46a72d9e8195"
    CLIENT_SECRET = "98254d2479944fed9ac4c4d2281e8de7"

    def get_token():
        auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        token_response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {b64_auth}"},
            data={"grant_type": "client_credentials"}
        )
        return token_response.json().get("access_token")

    def get_artist_data(artist_name, token):
        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": artist_name, "type": "artist", "limit": 1}
        response = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params)
        items = response.json().get('artists', {}).get('items')
        if items:
            artist = items[0]
            return {
                "name": artist['name'],
                "followers": artist['followers']['total'],
                "popularity": artist['popularity']
            }

    artist_names = [
        "Dua Lipa", "J. Cole", "Lana Del Rey", "Stray Kids", "Gigi Perez",
        "Nate Smith", "Alice In Chains", "Tommy Richman", "PARTYNEXTDOOR",
        "Red Hot Chili Peppers", "Megan Moroney", "Jason Aldean",
        "Creed", "JENNIE", "Dasha", "Lainey Wilson", "Journey", "Led Zeppelin"
    ]

    token = get_token()
    artist_data = []
    for name in artist_names:
        result = get_artist_data(name, token)
        if result:
            artist_data.append(result)

    with open("data.json", "w") as f:
        json.dump(artist_data, f, indent=4)

    conn = sqlite3.connect("SpotifyArtists.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS SpotifyArtists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            followers INTEGER,
            popularity INTEGER
        )
    ''')

    for artist in artist_data:
        c.execute('''
            INSERT INTO SpotifyArtists (name, followers, popularity)
            VALUES (?, ?, ?)
        ''', (artist['name'], artist['followers'], artist['popularity']))

    conn.commit()
    conn.close()

    df = pd.DataFrame(artist_data)
    df['log_followers'] = np.log10(df['followers'])

    X = df[['log_followers']]
    y = df['popularity']
    reg = LinearRegression().fit(X, y)
    df['predicted'] = reg.predict(X)
    df['residual'] = df['popularity'] - df['predicted']
    df['performance'] = df['residual'].apply(lambda x: 'Overperforming' if x > 3 else ('Underperforming' if x < -3 else 'On-Trend'))

    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=df,
        x='log_followers',
        y='popularity',
        hue='performance',
        palette={'Overperforming': 'green', 'Underperforming': 'red', 'On-Trend': 'gray'},
        s=100
    )
    sns.lineplot(x=df['log_followers'], y=df['predicted'], color='blue', label='Trendline')

    for _, row in df.iterrows():
        if abs(row['residual']) > 4:
            plt.text(row['log_followers'] + 0.01, row['popularity'] + 0.5, row['name'], fontsize=9)

    plt.title("Spotify Artists: Popularity vs. Followers (Log Scale)", fontsize=16)
    plt.xlabel("Log10(Followers)", fontsize=12)
    plt.ylabel("Popularity", fontsize=12)
    plt.legend(title="Performance")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("Visualizations/spotify_artist_visualization.png")
    plt.close()
