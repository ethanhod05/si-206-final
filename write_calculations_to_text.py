import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("this_one_works.db")

# 1. Calculate average concerts by popularity level
concerts_query = """
SELECT 
    pl.level AS PopularityLevel,
    uc.Concerts AS ConcertCount
FROM 
    SpotifyArtists sa
JOIN 
    PopularityLevel pl ON sa.popularity_level_id = pl.id
JOIN 
    UpcomingConcerts uc ON sa.name = uc.Name_id
"""
concert_df = pd.read_sql_query(concerts_query, conn)
avg_concerts = concert_df.groupby("PopularityLevel")["ConcertCount"].mean()

# 2. Calculate log10 of followers from Spotify data
spotify_query = "SELECT name, followers FROM SpotifyArtists WHERE followers > 0"
spotify_df = pd.read_sql_query(spotify_query, conn)
spotify_df['log_followers'] = np.log10(spotify_df['followers'])
avg_log_followers = spotify_df['log_followers'].mean()

conn.close()

# 3. Write results to a text file
with open("results.txt", "w") as f:
    f.write("Average Number of Upcoming Concerts by Popularity Level:\n")
    for level, avg in avg_concerts.items():
        f.write(f"{level}: {avg:.2f} concerts\n")
    
    f.write("\nAverage Log10 Followers Across All Spotify Artists:\n")
    f.write(f"{avg_log_followers:.2f}\n")
