import pandas as pd
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster

# Load the Excel file
file_path = '/Users/vinayayala/Desktop/Zen/Zen Staff Map.xlsx'
df = pd.read_excel(file_path)

# Initialize geolocator
geolocator = Nominatim(user_agent="zip_code_mapper")

# Create a map centered in the US
map_center = [38.0, -97.0]
us_map = folium.Map(location=map_center, zoom_start=5)

# Create a marker cluster
marker_cluster = MarkerCluster().add_to(us_map)

# Geocode zip codes and add to map
for index, row in df.iterrows():
    zip_code = row['Zip']  # Replace 'Zip Code' with the actual column name if different
    first_name = row['First Name']  # Replace 'First Name' with the actual column name if different
    last_name = row['Last Name']  # Replace 'Last Name' with the actual column name if different
    try:
        location = geolocator.geocode({'postalcode': zip_code, 'country': 'US'})
        if location:
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=f"{first_name} {last_name}\nZip Code: {zip_code}"
            ).add_to(marker_cluster)
    except Exception as e:
        print(f"Error geocoding {zip_code}: {e}")

# Add a red pin with a 50-mile radius circle at the specified coordinates
specified_location = [38.975868, -77.315613]
folium.Marker(
    location=specified_location,
    popup="Specified Location",
    icon=folium.Icon(color='red')
).add_to(us_map)
folium.Circle(
    location=specified_location,
    radius=80467,  # 50 miles in meters
    color='red',
    fill=True,
    fill_opacity=0.2
).add_to(us_map)

# Save the map to an HTML file
output_file_path = '/Users/vinayayala/Desktop/Zen/zip_code_map.html'
us_map.save(output_file_path)

print(f"Map has been saved to {output_file_path}")
