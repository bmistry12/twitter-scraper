import sys
import webbrowser
from os import getcwd
from time import sleep

from folium import Map
from folium.plugins import HeatMap
from geopy.geocoders import Nominatim

from utils import csv_to_df


def augment_locations(locations, counts):
    """Weigh each location by the tweets popularity."""
    augmented_loctions = []
    for i, location in enumerate(locations):
        augmented_loctions.extend([location for n in range(counts[i])])
    return list(filter((0, 0).__ne__, augmented_loctions))


def get_lat_long(location, app_map):
    """Converts text location to latitude and longitude."""
    sleep(0.5)
    try:
        raw_location = app_map.geocode(location).raw
        return raw_location["lat"], raw_location["lon"]
    except:  # noqa: E722
        return 0, 0


def heat_mapper():
    """Create heat map."""
    print("Stitiching your heat map together...")
    app_map = Nominatim(user_agent="tutorial")
    hmap = Map(location=[0, 0], zoom_start=3)
    counts = [int(x) for x in map_df["count"]]
    locations = [get_lat_long(x, app_map) for x in map_df["location"]]
    final_coord_list = augment_locations(locations, counts)
    hm_wide = HeatMap(
        final_coord_list,
        min_opacity=0.2,
        radius=17,
        blur=15,
        max_zoom=1,
    )
    hmap.add_child(hm_wide)
    return hmap


def save_map(hmap, file):
    """Save map to file and open it."""
    hmap.save(str(file))
    print(f"Opening {file} in your default web browser...")
    webbrowser.open(file)


if __name__ == "__main__":
    input_csv = str(sys.argv[1])
    map_df = csv_to_df(input_csv)
    heat_map = heat_mapper()
    output_file = getcwd() + "/" + input_csv.replace(".csv", ".html")
    save_map(heat_map, output_file)
