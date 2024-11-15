import sqlite3
import sys
from pathlib import Path

def initialize_database(db_name):
    # Check if database file exists
    db_exists = Path(db_name).exists()
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # If database exists, check if the required table exists
    if db_exists:
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='phonebook';''')
        table_exists = cursor.fetchone() is not None
    else:
        table_exists = False
    
    # If the required table does not exist, create it
    if not table_exists:
        cursor.execute('''CREATE TABLE phonebook (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            phone_number TEXT NOT NULL)''')
        conn.commit()
    
    return conn, cursor

def fetch_all_records(cursor):
    # Fetch all records from phonebook table
    cursor.execute('SELECT * FROM phonebook')
    records = cursor.fetchall()
    return records

def display_records(records):
    # Display records formatted nicely
    if records:
        print("\nPhonebook Records:")
        for record in records:
            print(f"ID: {record[0]}, Name: {record[1]}, Phone Number: {record[2]}")
    else:
        print("\nNo records found in the phonebook.")

def add_new_record(cursor, conn):
    # Prompt user for new record input
    name = input("\nEnter Name: ")
    phone_number = input("Enter Phone Number: ")
    
    # Insert new record into phonebook table
    cursor.execute('INSERT INTO phonebook (name, phone_number) VALUES (?, ?)', (name, phone_number))
    conn.commit()

def main():
    # Database file location
    db_name = "phonebook.db"
    
    # Initialize database and create connection
    conn, cursor = initialize_database(db_name)
    
    # Check command line arguments for mode selection
    if len(sys.argv) != 2:
        print("Usage: python script.py [list|new]")
        return
    
    mode = sys.argv[1]
    
    try:
        if mode == "list":
            # Fetch and display all records from the phonebook
            records = fetch_all_records(cursor)
            display_records(records)
        elif mode == "new":
            # Add a new record to the phonebook
            add_new_record(cursor, conn)
        else:
            print("Invalid mode. Use 'list' to display records or 'new' to add a record.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

if __name__ == "__main__":
    main()
