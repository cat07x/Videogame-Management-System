import pandas as pd
import sqlite3
import json  # to handle JSON-like structures

# Path to your Excel file
excel_file = 'output.xlsx'

# SQLite database connection
DATABASE = 'gaming_database.db'  # Your SQLite database file

def get_db_connection():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def import_tags_from_excel(excel_file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file)

    # Connect to the SQLite database
    conn = get_db_connection()

    # Iterate through each row in the Excel file's 'tags' column
    for index, row in df.iterrows():
        # Assuming the 'tags' column contains a string representation of a list of JSON objects
        tags_json = row['tags']
        
        try:
            # Parse the tags JSON (if it's a string, convert it into a Python list of dicts)
            tags_data = json.loads(tags_json) if isinstance(tags_json, str) else tags_json

            for tag in tags_data:
                tag_name = tag.get('name', None)
                
                if tag_name:
                    # Check if the tag already exists to prevent duplicates
                    existing_tag = conn.execute('SELECT * FROM Tags WHERE tag_name = ?', (tag_name,)).fetchone()
                    
                    if not existing_tag:
                        # Insert the tag name into the Tags table
                        conn.execute('INSERT INTO Tags (tag_name) VALUES (?)', (tag_name,))
                    else:
                        print(f"Tag '{tag_name}' already exists in the database.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in row {index}")
        except Exception as e:
            print(f"Unexpected error in row {index}: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Tag import completed.")

if __name__ == '__main__':
    import_tags_from_excel(excel_file)
