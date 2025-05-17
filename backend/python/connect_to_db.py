import sqlite3

def create_connection(db_file):
    """ Create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connection to SQLite DB successful: {db_file}")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    return conn

def close_connection(conn):
    """ Close the database connection """
    if conn:
        conn.close()
        print("Connection closed.")

# Usage
conn = create_connection("gaming_database.db")
close_connection(conn)
