import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('gaming_database.db')
    conn.row_factory = sqlite3.Row  # This helps in returning dictionaries instead of tuples
    return conn

# Function to create the Users table (if it doesn't exist)
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the Users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        profile_picture TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Function to insert a new user into the Users table
def signup_user(username, email, password, profile_picture=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the username or email already exists
    cursor.execute('SELECT * FROM Users WHERE username = ? OR email = ?', (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return "Username or Email already exists!"  # Return error message if user exists

    # Hash the password for security
    password_hash = generate_password_hash(password)

    # Insert the new user into the Users table
    cursor.execute('''
    INSERT INTO Users (username, email, password_hash, profile_picture)
    VALUES (?, ?, ?, ?)
    ''', (username, email, password_hash, profile_picture or ''))

    conn.commit()
    conn.close()

    return "User registered successfully!"

# Function to verify user credentials during login
def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user by username
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user_data = cursor.fetchone()

    if user_data is None:
        conn.close()
        return "Invalid username or password.", None

    # Check if the entered password matches the stored password hash
    stored_password_hash = user_data['password_hash']
    if check_password_hash(stored_password_hash, password):
        user = {
            'user_id': user_data['user_id'],
            'username': user_data['username'],
            'email': user_data['email'],
            'profile_picture': user_data['profile_picture']
        }
        conn.close()
        return "Login successful", user
    else:
        conn.close()
        return "Invalid username or password.", None
