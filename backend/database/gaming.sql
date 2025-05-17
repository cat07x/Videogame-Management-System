-- DROP DATABASE gamingdb;
-- DROP TABLE Users;
-- DROP TABLE Games;
-- DROP TABLE Reviews;

CREATE DATABASE gamingdb;
USE gamingdb;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,  -- for age verification
    join_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    profile_picture VARCHAR(255)
);

CREATE TABLE Games (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    release_date DATETIME NOT NULL,
    genre VARCHAR(50) NOT NULL,
    platform VARCHAR(50),
    stores VARCHAR(1000),
    description TEXT,
    age_rating ENUM('G', 'T', 'M', 'E') DEFAULT 'G'  -- for age rating
    update_date DATETIME
);

CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    review_id INT NOT NULL,
    user_id INT NOT NULL,
    comment_text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (review_id) REFERENCES Reviews(review_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE GameTags (
    game_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (game_id, tag_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id)
);

CREATE TABLE GameReviewsStatistics (
    game_id INT NOT NULL,
    total_reviews INT DEFAULT 0,
    average_rating DECIMAL(3, 2) DEFAULT 0.00,
    PRIMARY KEY (game_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

CREATE TABLE FavoriteGames (
    user_id INT NOT NULL,
    game_id INT NOT NULL,
    PRIMARY KEY (user_id, game_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

CREATE TABLE GameImages (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
);

ALTER TABLE Games MODIFY platform VARCHAR(1000);
ALTER TABLE Games MODIFY COLUMN age_rating ENUM('G', 'T', 'M', 'E') DEFAULT 'G';
ALTER TABLE Games CHANGE developer stores VARCHAR(100);
ALTER TABLE Games MODIFY stores VARCHAR(1000);
ALTER TABLE Games ADD developer VARCHAR(500);