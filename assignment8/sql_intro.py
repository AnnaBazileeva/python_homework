import sqlite3
import os

db_path = "../db/magazines.db"

try:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    print(f"Connected to database at {db_path}")

    cur = conn.cursor()

    cur.execute('''
         CREATE TABLE IF NOT EXISTS publishers (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL UNIQUE,
             address TEXT,
             phone TEXT,
             email TEXT
)
''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            publisher_id INTEGER NOT NULL,
            category TEXT,
            price DECIMAL(10,2) NOT NULL,
            description TEXT,
            FOREIGN KEY (publisher_id) REFERENCES publishers(id),
            UNIQUE(name, publisher_id)
    )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zip_code TEXT NOT NULL
    )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            payment_method TEXT,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id),
            UNIQUE(subscriber_id, magazine_id, start_date)
        )
        ''')


    conn.commit()
    print("Database tables created successfully!")
    print("Tables created:")
    print("- publishers")
    print("- magazines")
    print("- subscribers")
    print("- subscriptions")


except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed")

