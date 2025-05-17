import pandas as pd
import requests

def fetch_data_from_api(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def write_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def main():
    api_key = 'bbe2522574bc440492744ee3c09e0634'
    all_games = []
    page = 1
    target_count = 777  # Target number of games

    while len(all_games) < target_count:
        api_url = f'https://api.rawg.io/api/games?key={api_key}&page={page}'
        data = fetch_data_from_api(api_url)

        if data is None or not data.get('results'):
            break  # Exit if no more results or fetch failed

        all_games.extend(data['results'])
        page += 1  # Move to the next page

        # Optional: Check if there are fewer than 20 results
        if len(data['results']) < 20:
            break  # Exit if fewer results than expected, indicating no more pages

    # Limit to the target count
    all_games = all_games[:target_count]
    
    write_to_excel(all_games, 'games_data.xlsx')

if __name__ == '__main__':
    main()