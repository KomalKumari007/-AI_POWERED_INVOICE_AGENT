import sqlite3
import os

# Saving the relational database file in the same root folder
DB_PATH = "invoices.db"

def get_db_connection():
    """
    Creates and yields a synchronous database connection to the SQLite ledger file.
    """
    conn = sqlite3.connect(DB_PATH)
    # Enable accessing column records via explicit string headers rather than array indexes
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """
    Constructs the target audit data table schemas automatically if they do not exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build core historical audit logs table structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            vendor_name TEXT,
            total_amount REAL,
            status TEXT NOT NULL,
            audit_reason TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()