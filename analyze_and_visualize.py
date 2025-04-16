import sqlite3
import matplotlib.pyplot as plt

# Database name (must match what was created in your data_fetch.py)
DB_NAME = "music_data.db"

def analyze_data():
    """
    Connects to the database and performs a SQL JOIN query to retrieve:
    - Artist name from the Artists table
    - Total number of unique concert events from TicketmasterEvents
    - Maximum popularity score from SpotifyStats (represents most popular track)
    
    Results are saved to a text file for use in your final report.
    Returns:
        results (list of tuples): Each tuple includes (artist_name, event_count, top_popularity)
    """
    # Connect to SQLite database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # SQL JOIN across Artists, SpotifyStats, and TicketmasterEvents using shared artist_id
    query = '''
    SELECT A.name, 
           COUNT(DISTINCT T.id) AS event_count,
           (SELECT MAX(S.popularity) 
            FROM SpotifyStats S 
            WHERE S.artist_id = A.id) AS top_popularity
    FROM Artists A
    LEFT JOIN TicketmasterEvents T ON A.id = T.artist_id
    GROUP BY A.id
    '''

    cur.execute(query)
    results = cur.fetchall()
    conn.close()

    # Export the joined and calculated results to a .txt file
    with open("calculated_data.txt", "w") as f:
        for row in results:
            artist, events, popularity = row
            f.write(f"{artist}: {events} events, Top Track Popularity: {popularity}\n")

    return results

def visualize_data(results):
    """
    Takes the SQL query results and generates a scatterplot that compares:
    - X-axis: Top track popularity on Spotify
    - Y-axis: Number of concert events listed on Ticketmaster
    
    Saves the plot as an image file ("visualization.png") and displays it on screen.
    """
    # Parse the results into individual lists for plotting
    names = [r[0] for r in results]               # artist names
    events = [r[1] for r in results]              # number of Ticketmaster events
    popularity = [r[2] if r[2] is not None else 0 for r in results]  # top track popularity

    # Create the scatterplot
    plt.figure(figsize=(10, 6))
    plt.scatter(popularity, events)

    # Label each point with the artist name
    for i in range(len(names)):
        plt.annotate(names[i], (popularity[i], events[i]))

    # Label the axes and set title
    plt.xlabel("Top Track Popularity (Spotify)")
    plt.ylabel("Number of Concert Events (Ticketmaster)")
    plt.title("Spotify Popularity vs. Ticketmaster Events")

    # Add grid, format the layout, and save the plot as an image
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("visualization.png")
    plt.show()

# Run the full analysis pipeline when script is executed
if __name__ == "__main__":
    results = analyze_data()     # Step 1: Join and calculate
    visualize_data(results)      # Step 2: Create the graph
