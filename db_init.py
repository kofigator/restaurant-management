import sqlite3

def initialize_db():
    connection = sqlite3.connect('Order.db', check_same_thread=False)
    cursor = connection.cursor()
    
    # Create the Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID TEXT PRIMARY KEY,
        Username TEXT NOT NULL,
        Item TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        UnitPrice REAL NOT NULL,
        TotalPrice REAL NOT NULL,
        LogDate TEXT NOT NULL
    )
    ''')
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    initialize_db()
    print("Database initialized and Orders table created.")
