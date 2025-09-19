import sqlite3
import os

db_path = "../db/magazines.db"

os.makedirs("../db", exist_ok=True)

def create_connection():
    try:
        conn = sqlite3.connect("../db/magazines.db")
        print("Database created and connected successfully.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return None

def close_connection(conn):
    if conn:
        conn.close()
        print("Connection closed.")


def create_tables(conn):
    try:
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
                state TEXT NOT NULL
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

    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")


def add_publisher(conn, name, address, phone, email):
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM publishers WHERE name = ?", (name,))
        if cur.fetchone():
            print(f"Publisher '{name}' already exists.")
            return
        cur.execute(
            "INSERT INTO publishers (name, address, phone, email) VALUES (?, ?, ?, ?)",
            (name, address, phone, email),
        )
        conn.commit()
        print(f"Publisher '{name}' added.")
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding publisher: {e}")
        return None


def add_magazine(conn, name, publisher_id, category, price, description):
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM magazines WHERE name = ? AND publisher_id = ?",
            (name, publisher_id),
        )
        if cur.fetchone():
            print(f"Magazine '{name}' for publisher {publisher_id} already exists.")
            return
        cur.execute(
            """INSERT INTO magazines (name, publisher_id, category, price, description)
               VALUES (?, ?, ?, ?, ?)""",
            (name, publisher_id, category, price, description),
        )
        conn.commit()
        print(f"Magazine '{name}' added.")
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding magazine: {e}")
        return None


def add_subscriber(conn, first_name, last_name, email, phone, address, city, state):
    try:
        cur = conn.cursor()
        cur.execute(
            """SELECT id FROM subscribers
               WHERE first_name = ? AND last_name = ? AND address = ? AND city = ? AND state = ? """,
            (first_name, last_name, address, city, state),
        )
        if cur.fetchone():
            print(f"Subscriber {first_name} {last_name} at {address}, {city} already exists.")
            return
        cur.execute(
            """INSERT INTO subscribers
               (first_name, last_name, email, phone, address, city, state)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (first_name, last_name, email, phone, address, city, state),
        )
        conn.commit()
        print(f"Subscriber {first_name} {last_name} added.")
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding subscriber: {e}")
        return None


def add_subscription(conn, subscriber_id, magazine_id, start_date, end_date, payment_method):
    try:
        cur = conn.cursor()
        cur.execute(
            """SELECT id FROM subscriptions
               WHERE subscriber_id = ? AND magazine_id = ? AND start_date = ?""",
            (subscriber_id, magazine_id, start_date),
        )
        if cur.fetchone():
            print(f"Subscription already exists for subscriber {subscriber_id} and magazine {magazine_id}.")
            return None
        cur.execute(
            """INSERT INTO subscriptions
               (subscriber_id, magazine_id, start_date, end_date, payment_method)
               VALUES (?, ?, ?, ?, ?)""",
            (subscriber_id, magazine_id, start_date, end_date, payment_method),
        )
        conn.commit()
        print(f"Subscription added for subscriber {subscriber_id}.")
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding subscription: {e}")
        return None

def show_all_subscribers(conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscribers")
        rows = cursor.fetchall()
        print("\nAll subscribers:")
        for row in rows:
            print(row)

def show_all_magazines(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM magazines ORDER BY name")
    rows = cursor.fetchall()
    print("\nAll magazines:")
    for row in rows:
        print(row)

def show_magazines_by_publisher(conn, publisher_name):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.name
        FROM magazines m
        JOIN publishers p ON m.publisher_id = p.id
        WHERE p.name = ?
    """, (publisher_name,))
    rows = cursor.fetchall()
    print(f"\nMagazines by {publisher_name}:")
    for row in rows:
        print(row[0])

if __name__ == "__main__":
        try:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA foreign_keys = 1")
            print(f"Connected to database at {db_path}")

            create_tables(conn)

            publisher1_id = add_publisher(conn, "Times", "225 Liberty Street, New York, NY", "202-555-2255", "info@time.com")
            publisher2_id = add_publisher(conn, "Fox", "1 World Trade Center, Las Vegas, NV", "202-303-2233", "indo@fox.com")
            publisher3_id = add_publisher(conn, "National Geographic", "17th Street NW, Washington, DC", "202-203-7000", "info@natgeo.com")


            magazine1_id = add_magazine(conn, "Times", publisher1_id, "News", 5.99, "News and current affairs magazine")
            magazine2_id = add_magazine(conn, "Vogue", publisher2_id, "Fashion", 6.99, "Fashion and lifestyle magazine")
            magazine3_id = add_magazine(conn, "National Geographic", publisher3_id, "Science", 6.99,"Science and nature magazine")

            subscriber1_id = add_subscriber(conn, "John", "Smith", "john@email.com", "555-1010",
                                            "123 Main St", "New York", "NY")
            subscriber2_id = add_subscriber(conn, "Sarah", "Johnson", "sarah@email.com", "555-0102",
                                            "456 Old Road Ave", "Los Angeles", "CA")
            subscriber3_id = add_subscriber(conn, "Michael", "Brown", "mike@email.com", "202-0103",
                                            "789 Pine St", "Chicago", "IL")


            if subscriber1_id and magazine1_id:
                add_subscription(conn, subscriber1_id, magazine1_id, "2024-01-01", "2024-12-31",  "credit_card")
            if subscriber2_id and magazine2_id:
                add_subscription(conn, subscriber2_id, magazine2_id, "2024-01-15", "2024-12-15",  "paypal")
            if subscriber3_id and magazine1_id:
                add_subscription(conn, subscriber3_id, magazine1_id, "2024-03-01", "2024-12-31",  "check")

            conn.commit()
            print("\nDatabase populated successfully!")
            print("Added publishers, magazines, subscribers, and subscriptions.")

            show_all_subscribers(conn)
            show_all_magazines(conn)
            show_magazines_by_publisher(conn, "Fox")

            close_connection(conn)


        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            if 'conn' in locals() and conn:
                conn.close()
                print("Connection closed")
