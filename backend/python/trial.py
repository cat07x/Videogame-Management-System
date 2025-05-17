import sqlite3

def check_games_table():
    conn = sqlite3.connect('gaming_database.db')
    conn.row_factory = sqlite3.Row
    games = conn.execute('SELECT * FROM Games').fetchall()
    conn.close()

    for game in games:
        print(game['title'])

check_games_table()
