import csv
import requests

def fetch_data_from_api(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()  # Assuming the API returns JSON data

def write_to_csv(data, filename):
    if not data:
        print("No data to write to CSV.")
        return

    # Get the keys from the first dictionary for the header
    keys = data[0].keys()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def main():
    api_key = 'bbe2522574bc440492744ee3c09e0634'
    all_games = []
    page = 1
    target_count = 777  # Target number of games

    while len(all_games) < target_count:
        api_url = f'https://api.rawg.io/api/games?key={api_key}&page={page}'  # API key as query parameter
        data = fetch_data_from_api(api_url)
        
        # Assuming the API returns a list of games in 'results'
        games_data = data.get('results', [])
        
        if not games_data:
            break  # Exit if no more results
        
        all_games.extend(games_data)
        page += 1  # Move to the next page

        # Check if there are fewer results than expected
        if len(games_data) < 20:
            break  # Exit if fewer results than expected, indicating no more pages

    # Limit to the target count
    all_games = all_games[:target_count]
    
    write_to_csv(all_games, 'games_data.csv')

if __name__ == '__main__':
    main()
