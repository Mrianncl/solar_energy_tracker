# utils/db_utils.py
import sqlite3
import os

DB_PATH = "../data/users.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            type TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            monthly_saving REAL,
            co2_saved_yearly REAL,
            trees_saved REAL,
            date TEXT DEFAULT (date('now'))
        )
    ''')
    conn.commit()
    conn.close()