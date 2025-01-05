import requests
import pandas as pd
import time  # To manage rate limiting
from datetime import datetime

API_KEY = 'df200b4d75f8ab4646270a4059b2c26b'

# Define Schlager artists
SCHLAGER_ARTISTS = [
    "Michelle", "Udo Jürgens", "Wolfgang Petry", "Matthias Reim", "Roland Kaiser",
    "Heino", "Peggy March", "Howard Carpendale", "Juliane Werding", "Tino Martin",
    "Marianne Rosenberg", "Beatrice Egli", "Vicky Leandros", "Vanessa Mai", 
    "Jürgen Drews", "Michael Holm", "Rex Gildo", "Costa Cordalis"
]

# Define Pop artists
POP_ARTISTS = [
    "Taylor Swift", "Ed Sheeran", "Adele", "Justin Bieber", "Lady Gaga", "Rihanna",
    "Beyoncé", "Bruno Mars", "Katy Perry", "The Weeknd", "Dua Lipa", "Sam Smith",
    "Billie Eilish", "Harry Styles", "Shawn Mendes", "Selena Gomez", "Ariana Grande",
    "Post Malone", "Camila Cabello", "Doja Cat", "Olivia Rodrigo", "Miley Cyrus",
    "Lizzo", "Lana Del Rey", "Halsey", "Demi Lovato", "P!nk", "Ellie Goulding",
    "Charlie Puth", "Coldplay", "Imagine Dragons", "One Direction", "Maroon 5",
    "Sia", "Jason Derulo", "John Legend", "Zara Larsson", "Meghan Trainor", "Luis Fonsi",
    "Kygo", "Calvin Harris", "Avicii", "David Guetta", "Major Lazer", "Chainsmokers",
    "Shakira", "Pitbull", "Flo Rida", "Pharrell Williams", "Kelly Clarkson"
]

def get_artist_info(artist_name, api_key):
    """
    Fetches detailed information for a specific artist from the Last.fm API.
    """
    url = f'http://ws.audioscrobbler.com/2.0/?method=artist.getInfo&artist={artist_name}&api_key={api_key}&format=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'artist' in data and 'stats' in data['artist']:
            stats = data['artist']['stats']
            return int(stats.get('listeners', 0)), int(stats.get('playcount', 0))
    else:
        print(f"Error fetching info for {artist_name}: {response.status_code}")
    return 0, 0  # Default values if the API call fails

def fetch_historical_data(artists, api_key, start_year, end_year):
    """
    Fetches historical listener and play count data for a list of artists over a specified timeframe.
    """
    historical_data = []
    for artist in artists:
        print(f"Fetching data for artist: {artist}")
        for year in range(start_year, end_year + 1):
            try:
                listeners, playcount = get_artist_info(artist, api_key)
                historical_data.append({
                    'Artist': artist,
                    'Year': year,
                    'Listeners': listeners,
                    'Playcount': playcount
                })
                print(f"Year {year}: {listeners} listeners, {playcount} playcount for {artist}")
            except Exception as e:
                print(f"Error fetching data for {artist} in year {year}: {e}")
            time.sleep(0.2)  # To avoid hitting API rate limits

    return pd.DataFrame(historical_data)

if __name__ == "__main__":
    start_year = 2007
    end_year = 2024

    # Fetch Schlager artists data
    schlager_data = fetch_historical_data(SCHLAGER_ARTISTS, API_KEY, start_year, end_year)
    if not schlager_data.empty:
        schlager_data.to_csv('data/schlager_historical_data.csv', index=False)
        print("\nSchlager Artists Historical Data:")
        print(schlager_data)
    else:
        print("No historical data retrieved for Schlager artists.")

    # Fetch Pop artists data
    pop_data = fetch_historical_data(POP_ARTISTS, API_KEY, start_year, end_year)
    if not pop_data.empty:
        pop_data.to_csv('data/pop_historical_data.csv', index=False)
        print("\nPop Artists Historical Data:")
        print(pop_data)
    else:
        print("No historical data retrieved for Pop artists.")

    # Merge datasets and calculate correlation
    if not schlager_data.empty and not pop_data.empty:
        merged_data = pd.concat([schlager_data.assign(Category='Schlager'),
                                 pop_data.assign(Category='Pop')])
        correlation_matrix = merged_data[['Listeners', 'Playcount']].corr()
        print("\nCorrelation Matrix (Listeners and Playcount):")
        print(correlation_matrix)

        # Save correlation matrix
        correlation_matrix.to_csv('data/correlation_matrix.csv')