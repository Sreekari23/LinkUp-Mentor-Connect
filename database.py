import sqlite3
from sqlite3 import Connection

def get_connection() -> Connection:
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect('mentor_connect.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create the necessary tables for user and activities management."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            password TEXT,
            email TEXT,
            is_mentor INTEGER DEFAULT 0,  -- 1 if the user is a mentor
            is_mentee INTEGER DEFAULT 0   -- 1 if the user is a mentee
        )
    ''')

    # Create activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            type TEXT,
            with_user TEXT,
            date TEXT,
            time TEXT,
            status TEXT,
            role TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_user(user_id: str, password: str, email: str, is_mentor: int, is_mentee: int):
    """Add a new user to the users table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, password, email, is_mentor, is_mentee) VALUES (?, ?, ?, ?, ?)',
                   (user_id, password, email, is_mentor, is_mentee))
    conn.commit()
    conn.close()

def get_user(user_id: str):
    """Retrieve user data by user_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    print(f"Debug: Fetched user data: {user}")  # Debugging print
    conn.close()
    return user

def add_activity(user_id: str, activity_type: str, with_user: str, date: str, time: str, status: str, role: str):
    """Add a new activity to the activities table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO activities (user_id, type, with_user, date, time, status, role) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (user_id, activity_type, with_user, date, time, status, role))
    conn.commit()
    conn.close()

def get_activities(user_id: str):
    """Retrieve all activities for a given user_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM activities WHERE user_id = ?', (user_id,))
    activities = cursor.fetchall()
    conn.close()
    return activities

def print_all_users():
    """Print all users in the users table for debugging purposes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    for user in users:
        print(dict(user))
    conn.close()
