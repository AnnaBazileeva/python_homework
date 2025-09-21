import sqlite3
import pandas as pd
import os

db_path = "../db/lesson.db"

os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = 1")

conn.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL NOT NULL
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS line_items (
    line_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

conn.execute("INSERT INTO products (product_name, price) VALUES ('Apple', 1.2)")
conn.execute("INSERT INTO products (product_name, price) VALUES ('Banana', 0.8)")
conn.execute("INSERT INTO products (product_name, price) VALUES ('Orange', 1.5)")

conn.execute("INSERT INTO line_items (product_id, quantity) VALUES (1, 10)")
conn.execute("INSERT INTO line_items (product_id, quantity) VALUES (2, 5)")
conn.execute("INSERT INTO line_items (product_id, quantity) VALUES (3, 8)")

conn.commit()

conn.commit()

def main():
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
    if tables.empty:
        print("No tables found in database.")
        return

    line_items_exist = pd.read_sql_query("SELECT COUNT(*) as cnt FROM sqlite_master WHERE name='line_items'", conn)['cnt'][0]
    products_exist = pd.read_sql_query("SELECT COUNT(*) as cnt FROM sqlite_master WHERE name='products'", conn)['cnt'][0]

    if line_items_exist == 0 or products_exist == 0:
        print("Required tables exist but are empty. No data to process.")
        return

    sql_query = """
    SELECT li.line_item_id, li.quantity, li.product_id, 
           p.product_name, p.price
    FROM line_items li
    JOIN products p ON li.product_id = p.product_id
    """
    try:
        df = pd.read_sql_query(sql_query, conn)
    except pd.io.sql.DatabaseError as e:
        print(f"Error reading data: {e}")
        return

    if df.empty:
        print("No line items found.")
        return

    print("Initial DataFrame:\n", df.head())

    df['total'] = df['quantity'] * df['price']
    print("\nWith Total Column:\n", df.head())

    summary = df.groupby('product_id').agg({
        'line_item_id': 'count',
        'total': 'sum',
        'product_name': 'first'
    }).reset_index()

    summary = summary.sort_values(by='product_name')
    print("\nGrouped Summary:\n", summary.head())

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "csv")
    os.makedirs(output_dir, exist_ok=True)

    summary.to_csv(os.path.join(output_dir, "order_summary.csv"), index=False)
print("\nSummary saved to csv/order_summary.csv")

if __name__ == "__main__":
    main()
    conn.close()
