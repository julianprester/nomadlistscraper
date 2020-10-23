import pandas as pd
from bs4 import BeautifulSoup

# Create empty pandas dataframe with one column "city"
df = pd.DataFrame(columns=['city'])

# Parse local cities.xml file with BeautifulSoup
soup = BeautifulSoup(open('data/raw/cities.xml', 'r', encoding='utf-8'), 'html.parser')

# Look for and loop over all <li> tags
cities = soup.find_all('li', {'class', 'item'})
for city in cities:
    if city.has_attr('data-slug'): # City name is in the "data-slug" attribute
        city_name = city['data-slug']

        # Add one row to pandas dataframe
        df = df.append({'city': city_name}, ignore_index=True)

# Save dataframe to cities csv file
df.to_csv('data/interim/cities.csv', index=False)
