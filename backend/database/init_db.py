import mysql.connector

# Database connection configuration
db_config = {
    'host': 'localhost',  # Replace with your Windows IP address
    'port': '3306',
    'user': 'root',              # Replace with your MySQL username
    'password': '0713',          # Replace with your MySQL password
    'database': 'gamingdb'                # The database you want to use
}

# Function to connect to the database
def connect_to_db(config):
    return mysql.connector.connect(**config)

def initialize_database():
    db_connection = connect_to_db(db_config)
    cursor = db_connection.cursor()
    
    # Run SQL commands to create tables
    with open("schema.sql", "r") as file:
        sql_script = file.read()
    
    for statement in sql_script.split(';'):
        if statement.strip():  # Execute only non-empty statements
            cursor.execute(statement)
    
    db_connection.commit()
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    initialize_database()
