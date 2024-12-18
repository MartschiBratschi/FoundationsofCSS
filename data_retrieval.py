import requests
import pandas as pd

API_KEY = 'df200b4d75f8ab4646270a4059b2c26b'
GENRE = 'schlager'

def get_top_artists_by_genre(genre, api_key, limit=50):
    url = f'http://ws.audioscrobbler.com/2.0/?method=tag.getTopArtists&tag={genre}&api_key={api_key}&format=json&limit={limit}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        artists = [(artist['name'], int(artist['listeners'])) for artist in data['topartists']['artist']]
        return pd.DataFrame(artists, columns=['Artist', 'Listeners'])
    else:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = get_top_artists_by_genre(GENRE, API_KEY)
    df.to_csv('data/schlager_artists.csv', index=False)
    print(df)
