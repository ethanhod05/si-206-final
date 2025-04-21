import spotify_artist_visualization
import heatmap
import dualaxisgraph
import calculate_concert_density

def run_all_visualizations():
    print("Running Spotify Artist Scatterplot & Regression...")
    spotify_artist_visualization.generate_visualization()

    print("Generating Heatmap...")
    heatmap.generate_heatmap()

    print("Creating Dual Axis Graph...")
    dualaxisgraph.generate_dual_axis_graph()

    print("Calculating Concert Density & Creating Bar Chart...")
    calculate_concert_density.generate_concert_density_chart()

    print("All visualizations saved to the Visualizations/ folder.")

if __name__ == "__main__":
    run_all_visualizations()
