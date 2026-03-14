import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT
            )
        """)
        
        # Categories table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        
        # Products table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_url TEXT,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)
        
        # Orders table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                items TEXT NOT NULL,
                total_price REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        self.connection.commit()

    def add_user(self, user_id, username, full_name):
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id, username, full_name) VALUES (?, ?, ?)", 
                            (user_id, username, full_name))
        self.connection.commit()

    def get_categories(self):
        return self.cursor.execute("SELECT * FROM categories").fetchall()

    def get_products_by_category(self, category_id):
        return self.cursor.execute("SELECT * FROM products WHERE category_id = ?", (category_id,)).fetchall()

    def add_order(self, user_id, items, total_price):
        self.cursor.execute("INSERT INTO orders (user_id, items, total_price) VALUES (?, ?, ?)", 
                            (user_id, items, total_price))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_user_orders(self, user_id):
        return self.cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()

db = Database('store.db')
