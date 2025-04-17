import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def generate_concert_density_chart():
    # Connect to your database
    conn = sqlite3.connect("this_one_works.db")

    # Join SpotifyArtists, PopularityLevel, and UpcomingConcerts
    query = """
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

    # Load data into a DataFrame
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Group by popularity level and calculate average concerts
    avg_concerts = df.groupby("PopularityLevel")["ConcertCount"].mean().reset_index()

    # Ensure consistent order
    level_order = ["Low", "Mid", "High"]
    avg_concerts["PopularityLevel"] = pd.Categorical(avg_concerts["PopularityLevel"], categories=level_order, ordered=True)
    avg_concerts = avg_concerts.sort_values("PopularityLevel")

    # Plot the results
    plt.figure(figsize=(8, 6))
    plt.bar(avg_concerts["PopularityLevel"], avg_concerts["ConcertCount"])
    plt.xlabel("Popularity Level")
    plt.ylabel("Average Number of Upcoming Concerts")
    plt.title("Average Concerts by Artist Popularity Level")
    plt.tight_layout()
    plt.savefig("Visualizations/concerts_by_popularity_level.png")
    plt.close()
