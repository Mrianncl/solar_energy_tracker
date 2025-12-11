# app/auth.py
import sqlite3
from utils.db_utils import DB_PATH, init_db

# Simulated active sessions
active_sessions = {}

def register_user(username, password, user_type):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, type) VALUES (?, ?, ?)",
                  (username, password, user_type))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        # Store session
        active_sessions[username] = True
        return {"id": user[0], "username": user[1], "type": user[3]}
    return None

def logout_user(username):
    if username in active_sessions:
        del active_sessions[username]