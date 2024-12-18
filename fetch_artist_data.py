import requests
import pandas as pd

def get_user_weekly_artist_chart(user, api_key):
    url = f'http://ws.audioscrobbler.com/2.0/?method=user.getWeeklyArtistChart&user={'bruhsini'}&api_key={'df200b4d75f8ab4646270a4059b2c26b'}&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return {}

# Replace 'USERNAME' with a real Last.fm username
data = get_user_weekly_artist_chart('bruhsini', 'df200b4d75f8ab4646270a4059b2c26b')
print(data)
