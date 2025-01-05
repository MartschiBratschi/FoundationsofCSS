import requests
import pandas as pd

def get_user_weekly_artist_chart(user, api_key, from_date=None, to_date=None):
    
    url = f'http://ws.audioscrobbler.com/2.0/?method=user.getWeeklyArtistChart&user={user}&api_key={api_key}&format=json'

    # Append date parameters if provided
    if from_date:
        url += f'&from={from_date}'
    if to_date:
        url += f'&to={to_date}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'weeklyartistchart' in data and 'artist' in data['weeklyartistchart']:
            # Parse the artist data into a DataFrame
            artists = data['weeklyartistchart']['artist']
            print("Raw artist data:", artists)  # Debugging line

            # Create a DataFrame with the available data
            df = pd.DataFrame(artists)
            required_columns = ['name', 'playcount', 'url']
            
            # Check if required columns exist
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                print(f"Warning: Missing columns {missing_columns} in the API response.")
                return df
            
            return df[required_columns]
        else:
            print("No artist data found in the response.")
            return pd.DataFrame()
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return pd.DataFrame()
if __name__ == '__main__':
    # Replace with your actual API key
    API_KEY = 'df200b4d75f8ab4646270a4059b2c26b'
    USER = 'bruhsini'

    # Example 1: Fetch weekly artist chart without date filters
    print("Fetching weekly artist chart without date filters:")
    weekly_chart = get_user_weekly_artist_chart(USER, API_KEY)
    print(weekly_chart)

    # Example 2: Fetch weekly artist chart with specific date range
    print("\nFetching weekly artist chart with date filters:")
    # Example Unix timestamps (convert your desired dates to Unix format if needed)
    from_date = '1672444800'  # 2023-01-01
    to_date = '1675123200'    # 2023-02-01
    weekly_chart_with_dates = get_user_weekly_artist_chart(USER, API_KEY, from_date=from_date, to_date=to_date)
    print(weekly_chart_with_dates)