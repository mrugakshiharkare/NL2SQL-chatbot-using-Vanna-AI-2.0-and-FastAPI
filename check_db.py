import sqlite3

try:
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\n---DATABASE VERIFICATION---")
    if not tables:
        print("No tables found! The batabase might be empty.")
    else:
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"-> {table[0]}")
            
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {e}")
    