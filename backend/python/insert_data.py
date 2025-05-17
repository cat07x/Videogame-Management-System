import pandas as pd
import sqlite3
import json
from werkzeug.security import generate_password_hash

# Function to create the database schema (including the Games and Users tables)
def create_schema(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Games (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        release_date TEXT,
        developer TEXT,
        background_image TEXT,
        rating REAL,
        ratings TEXT,
        ratings_count INTEGER,
        reviews_text_count INTEGER,
        added TEXT,
        added_by_status TEXT,
        metacritic INTEGER,
        playtime INTEGER,
        updated TEXT,
        reviews_count INTEGER,
        platforms TEXT,
        genre TEXT,
        stores TEXT,
        tags TEXT,
        age_rating TEXT,
        short_screenshots TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        join_date TEXT DEFAULT CURRENT_TIMESTAMP,
        profile_picture TEXT
    )
    ''')

# Function to insert data into the Games table
def insert_game_data(cursor, game):
    game_data = {
        'title': game.get('title', ''),
        'description': game.get('description', ''),
        'release_date': game.get('release_date', ''),
        'developer': game.get('developer', ''),
        'background_image': game.get('background_image', ''),
        'rating': game.get('rating', None),
        'ratings': json.dumps(game.get('ratings', [])),
        'ratings_count': game.get('ratings_count', 0),
        'reviews_text_count': game.get('reviews_text_count', 0),
        'added': game.get('added', ''),
        'added_by_status': game.get('added_by_status', ''),
        'metacritic': game.get('metacritic', 0),
        'playtime': game.get('playtime', 0),
        'updated': game.get('updated', ''),
        'reviews_count': game.get('reviews_count', 0),
        'platforms': json.dumps(game.get('platforms', [])),
        'genre': game.get('genre', ''),
        'stores': json.dumps(game.get('stores', [])),
        'tags': json.dumps(game.get('tags', [])),
        'age_rating': game.get('age_rating', ''),
        'short_screenshots': json.dumps(game.get('short_screenshots', []))
    }

    cursor.execute('''
    INSERT INTO Games (
        title, description, release_date, developer, background_image, rating, 
        ratings, ratings_count, reviews_text_count, added, added_by_status, metacritic, 
        playtime, updated, reviews_count, platforms, genre, stores, tags, age_rating, 
        short_screenshots
    ) VALUES (
        :title, :description, :release_date, :developer, :background_image, :rating, 
        :ratings, :ratings_count, :reviews_text_count, :added, :added_by_status, :metacritic, 
        :playtime, :updated, :reviews_count, :platforms, :genre, :stores, :tags, :age_rating, 
        :short_screenshots
    )''', game_data)

# Function to insert data into the Users table
def insert_user_data(cursor, user):
    user_data = {
        'username': user.get('username', ''),
        'email': user.get('email', ''),
        'password_hash': generate_password_hash(user.get('password', '')),  # Hash the password
        'profile_picture': user.get('profile_picture', '')
    }

    cursor.execute('''
    INSERT INTO Users (username, email, password_hash, profile_picture)
    VALUES (:username, :email, :password_hash, :profile_picture)
    ''', user_data)

# Main function to load data and insert it
def main():
    # Load Excel data (adjust to your file path)
    df_games = pd.read_excel('/home/riyavan/DBMS/games_data.xlsx', sheet_name='Games')
    
    # Check if 'Users' sheet exists before trying to load it
    try:
        df_users = pd.read_excel('/home/riyavan/DBMS/games_data.xlsx', sheet_name='Users')
    except ValueError:
        print("No 'Users' sheet found in the Excel file. Skipping user data import.")
        df_users = pd.DataFrame()  # This will be an empty DataFrame

    # Open SQLite database connection
    conn = sqlite3.connect('gaming_database.db')
    cursor = conn.cursor()
    
    # Create schema if not exists
    create_schema(cursor)
    
    # Insert game data
    for index, row in df_games.iterrows():
        game = row.to_dict()
        try:
            insert_game_data(cursor, game)
            print(f"Successfully inserted game: {game['title']}")
        except Exception as e:
            print(f"Error while processing game {game['title']}: {e}")

    # Insert user data if users sheet exists
    if not df_users.empty:
        for index, row in df_users.iterrows():
            user = row.to_dict()
            try:
                insert_user_data(cursor, user)
                print(f"Successfully inserted user: {user['username']}")
            except Exception as e:
                print(f"Error while processing user {user['username']}: {e}")

    # Commit and close
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
