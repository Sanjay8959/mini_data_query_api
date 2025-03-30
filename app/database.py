import sqlite3
from sqlite3 import Error
import os

# Global connection object
conn = None

def get_db_connection():
    """Return the database connection object"""
    global conn
    if conn is None:
        init_db()
    return conn

def init_db():
    """Initialize the in-memory SQLite database with mock data"""
    global conn
    try:
        # Create an in-memory database
        conn = sqlite3.connect(':memory:', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        
        # Create tables and insert mock data
        create_tables()
        insert_mock_data()
        
        print("Database initialized successfully")
        return conn
    except Error as e:
        print(f"Database initialization error: {e}")
        return None

def create_tables():
    """Create the necessary tables for our mock data"""
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        signup_date TEXT NOT NULL
    )
    ''')
    
    # Create products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        inventory INTEGER NOT NULL
    )
    ''')
    
    # Create sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        sale_date TEXT NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    
    conn.commit()

def insert_mock_data():
    """Insert mock data into the tables"""
    cursor = conn.cursor()
    
    # Insert customers
    customers = [
        (1, 'John Doe', 'john@example.com', '2023-01-15'),
        (2, 'Jane Smith', 'jane@example.com', '2023-02-20'),
        (3, 'Bob Johnson', 'bob@example.com', '2023-03-10'),
        (4, 'Alice Brown', 'alice@example.com', '2023-04-05'),
        (5, 'Charlie Davis', 'charlie@example.com', '2023-05-12')
    ]
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', customers)
    
    # Insert products
    products = [
        (1, 'Laptop', 'Electronics', 1200.00, 50),
        (2, 'Smartphone', 'Electronics', 800.00, 100),
        (3, 'Headphones', 'Electronics', 150.00, 200),
        (4, 'T-shirt', 'Clothing', 25.00, 500),
        (5, 'Jeans', 'Clothing', 45.00, 300),
        (6, 'Sneakers', 'Footwear', 80.00, 150),
        (7, 'Coffee Maker', 'Home Appliances', 120.00, 75),
        (8, 'Blender', 'Home Appliances', 60.00, 100)
    ]
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products)
    
    # Insert sales
    sales = [
        (1, 1, 1, 1, '2023-06-10', 1200.00),
        (2, 2, 2, 2, '2023-06-15', 1600.00),
        (3, 3, 3, 1, '2023-06-20', 150.00),
        (4, 4, 4, 3, '2023-07-05', 75.00),
        (5, 5, 5, 2, '2023-07-10', 90.00),
        (6, 1, 6, 1, '2023-07-15', 80.00),
        (7, 2, 7, 1, '2023-07-20', 120.00),
        (8, 3, 8, 2, '2023-07-25', 120.00),
        (9, 4, 1, 1, '2023-08-01', 1200.00),
        (10, 5, 2, 1, '2023-08-05', 800.00)
    ]
    cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)', sales)
    
    conn.commit()

def execute_query(query, params=()):
    """Execute a query and return the results"""
    try:
        cursor = get_db_connection().cursor()
        cursor.execute(query, params)
        
        # Check if this is a SELECT query
        if query.strip().upper().startswith('SELECT'):
            columns = [description[0] for description in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        else:
            get_db_connection().commit()
            return {"affected_rows": cursor.rowcount}
    except Error as e:
        print(f"Query execution error: {e}")
        return None
