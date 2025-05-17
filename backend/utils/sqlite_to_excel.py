import sqlite3
import pandas as pd

# Step 1: Connect to your SQLite database
db_file = 'gaming_database.db'  # Path to your SQLite file
conn = sqlite3.connect(db_file)

# Step 2: Get the list of tables in the SQLite database
tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(tables_query, conn)

# Step 3: Loop through each table and export it to Excel
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    for table in tables['name']:
        # Query to get all data from the current table
        query = f"SELECT * FROM {table}"
        
        # Load the data into a pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Write the DataFrame to an Excel sheet
        df.to_excel(writer, sheet_name=table, index=False)

# Step 4: Close the database connection
conn.close()

print("SQLite database has been successfully converted to Excel.")
