from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os
from backend.python.user_management import signup_user, login_user, create_users_table  # Import the new functions
import sqlite3

# Ensure this path matches your actual folder structure
app = Flask(__name__, 
            static_folder=os.path.join('frontend', 'static'), 
            template_folder=os.path.join('frontend', 'templates'))

# Set a secret key for session handling (necessary for using session)
app.secret_key = os.urandom(24)  # A random key for session

def get_db_connection():
    conn = sqlite3.connect('gaming_database.db')
    conn.row_factory = sqlite3.Row  # This makes it return rows as dictionaries
    return conn

# Initialize the database and create the Users table if not already done
create_users_table()

# Home page that displays the list of all games
@app.route('/')
def index():
    # Check if the user is logged in by checking the session
    username = session.get('username', None)
    
    # Fetch the distinct list of genres from the database
    conn = get_db_connection()
    genres = conn.execute('SELECT DISTINCT genre FROM Games').fetchall()  # Fetch all distinct genres
    conn.close()

    # Fetch the list of games from the database
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM Games').fetchall()  # Fetch all games
    conn.close()

    # Pass the session username and the games list to the template
    return render_template('index.html', genres=genres, games=games, search_query="", username=username)

# Game details page
@app.route('/game/<int:game_id>', methods=['GET', 'POST'])
def game_details(game_id):
    conn = get_db_connection()
    game = conn.execute('SELECT * FROM Games WHERE game_id = ?', (game_id,)).fetchone()

    if game is None:
        flash("Game not found!")
        return redirect(url_for('index'))

    reviews = conn.execute('''
        SELECT r.review_id, r.user_id, r.rating, r.review_text, r.created_at, u.username 
        FROM Reviews r
        JOIN Users u ON r.user_id = u.user_id
        WHERE r.game_id = ?
        ORDER BY r.created_at ASC
    ''', (game_id,)).fetchall()

    conn.close()
    
    reviews_list = [dict(review) for review in reviews]

    # Handle review submission (POST request)
    if request.method == 'POST' and 'rating' in request.form and 'review' in request.form:
        if 'user_id' in session:
            rating = request.form['rating']
            review_text = request.form['review']
            user_id = session['user_id']

            # Insert new review into the database
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO Reviews (game_id, user_id, rating, review_text, created_at) 
                VALUES (?, ?, ?, ?, ?)
            ''', (game_id, user_id, rating, review_text, datetime.utcnow()))
            conn.commit()
            conn.close()

            flash("Your review has been added successfully.", 'success')
            return redirect(url_for('game_details', game_id=game_id))
        else:
            flash("You must be logged in to leave a review.", 'danger')

    # Pass the game details and reviews to the template
    return render_template('game_details.html', game=game, reviews=reviews_list)


# Edit Review page
@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to edit a review.", 'danger')
        return redirect(url_for('index'))

    # Get the review from the database
    conn = get_db_connection()
    review = conn.execute('''
        SELECT * FROM Reviews WHERE review_id = ? AND user_id = ?
    ''', (review_id, session['user_id'])).fetchone()

    if review is None:
        flash("Review not found or you don't have permission to edit it.", 'danger')
        return redirect(url_for('game_details', game_id=review['game_id']))

    if request.method == 'POST':
        # Handle the form submission for editing the review
        rating = request.form['rating']
        review_text = request.form['review']

        conn.execute('''
            UPDATE Reviews SET rating = ?, review_text = ?, created_at = ? WHERE review_id = ?
        ''', (rating, review_text, datetime.utcnow(), review_id))
        conn.commit()
        conn.close()

        flash("Your review has been updated successfully.", 'success')
        return redirect(url_for('game_details', game_id=review['game_id']))

    # Pass the review data to the template
    return render_template('edit_review.html', review=review)



# Delete Review functionality
@app.route('/delete_review/<int:review_id>', methods=['GET'])
def delete_review(review_id):
    if 'user_id' in session:
        conn = get_db_connection()
        conn.execute('DELETE FROM Reviews WHERE review_id = ? AND user_id = ?', (review_id, session['user_id']))
        conn.commit()
        conn.close()
        flash("Review deleted successfully", 'success')
        return redirect(request.referrer)  # Redirect back to the same page
    flash("You must be logged in to delete a review.", 'danger')
    return redirect(url_for('index'))


# Search page to display games based on search query
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the search query from the request
    # Fetch games from the database based on the query
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM Games WHERE title LIKE ?', ('%' + query + '%',)).fetchall()
    conn.close()

    # Get the logged-in user's username if available
    username = session.get('username', None)

    return render_template('index.html', games=games, search_query=query, username=username)


# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        profile_picture = request.form.get('profile_picture', None)
        
        # Call the signup_user function to handle the signup
        result = signup_user(username, email, password, profile_picture)
        
        # Flash the result message
        flash(result)
        
        if "User registered successfully" in result:
            return redirect(url_for('login'))  # Redirect to login page after successful signup
        
    return render_template('signup.html')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Call the login_user function to check credentials
        result, user = login_user(username, password)
        
        flash(result)  # Display the result message
        
        if "successful" in result:
            # Save the user in session if login is successful
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session.permanent = True  # Make the session permanent

            return redirect(url_for('index'))  # Redirect to homepage after successful login
        else:
            return redirect(url_for('login'))

    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear session to log out the user
    return redirect(url_for('index'))  # Redirect to the home page after logout


# Genre-specific games route
@app.route('/genre/<genre>')
def games_by_genre(genre):
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM Games WHERE genre = ?', (genre,)).fetchall()
    conn.close()

    return render_template('genre_games.html', genre=genre, games=games)


# User profile route
@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("You need to log in to view your profile.", 'danger')
        return redirect(url_for('login'))

    # Get the logged-in user's ID from session
    user_id = session['user_id']

    # Connect to the database
    conn = get_db_connection()

    # Get user details (username, email, profile picture)
    user = conn.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,)).fetchone()

    # Get the user's reviews (game title, rating, review text)
    reviews = conn.execute('''
        SELECT r.review_id, g.title, r.rating, r.review_text, r.created_at
        FROM Reviews r
        JOIN Games g ON r.game_id = g.game_id
        WHERE r.user_id = ?
    ''', (user_id,)).fetchall()

    conn.close()

    # If user not found
    if user is None:
        flash("User not found.", 'danger')
        return redirect(url_for('index'))

    # Pass user details and reviews to the template
    return render_template('profile.html', user=user, reviews=reviews)


if __name__ == '__main__':
    app.run(debug=True)
