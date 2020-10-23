import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json

# Base URL for this scraping task with placeholder
base_url = 'https://nomadlist.com/{}'

# Regular expression for the "tripsCoords" JavaScript variable
p_coords = re.compile('var tripsCoords=(.*?);')

# Create empty pandas dataframe with 13 columns
df_trips = pd.DataFrame(columns=['city', 'city_slug', 'epoch_end', 'epoch_start', 'latitude', 'longitude', 'previous_latitude', 'previous_longitude', 'trip_id', 'trip_length', 'user_image', 'mode', 'user'])

# Read dataframe from users csv file
df_users = pd.read_csv('data/interim/users.csv')

# Loop over all users in the dataframe
for index, row in df_users.iterrows():
    print("{}/{}".format(index, len(df_users.index)))
    
    # Request url with user name appended and parse with BeautifulSoup
    response = requests.get(base_url.format(row[0]))
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for and loop over all <script> tags
    scripts = soup.find_all('script')
    for script in scripts:

        # Search for the regular expression inside the <script> tag
        match = p_coords.search(script.prettify())
        if match:

            # If found, turn into Python dictionary
            content = json.loads(match.groups()[0])
            if content:

                # Load the trips into a list of dictionaries
                trips = list(content.values())[0]

                # Add username to every trip
                trips_with_username = [dict(trip, **{'user':row[0]}) for trip in trips]
                
                # Append list of trips to the trips dataframe
                df_trips = df_trips.append(trips_with_username)

# Save dataframe to trips csv file
df_trips.to_csv('data/interim/trips.csv', index=False)
