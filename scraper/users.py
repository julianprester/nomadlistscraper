import pandas as pd
import requests
from bs4 import BeautifulSoup

# Base URL for this scraping task with placeholder
base_url = 'https://nomadlist.com/people/{}'

# Read dataframe from cities csv file
df_cities = pd.read_csv('data/interim/cities.csv')
user_list = [] # Empty list for a set of users

# Loop over all cities in the dataframe
for index, row in df_cities.iterrows():
    print("{}/{}".format(index, len(df_cities.index)))

    # Request url with city name appended and parse with BeautifulSoup
    try:
        response = requests.get(base_url.format(row[0]))
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for and loop over all <a> tags
        users = soup.find_all('a', {'class': 'no-border'})
        for user in users:
            if user.has_attr('href') and user['href'].startswith('/@'): # User name is in the "href" attribute and starts with "/@"
                user_name = user['href'][1:]
                user_list.append(user_name) # Add user name to user list

        # Remove duplicate user names (users can visit multiple cities)
        user_list = list(set(user_list))
    except:
        print(row[0])

# Create pandas dataframe from list and save to users csv file
df_users = pd.DataFrame(user_list, columns=['user'])
df_users.to_csv('data/interim/users.csv', index=False)
