# Secure Token Management, Expiration & Refresh
import sqlite3
import time

def store_token(user_id, access_token, refresh_token, expires_in):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens (
        user_id INTEGER PRIMARY KEY,
        access_token TEXT NOT NULL,
        refresh_token TEXT,
        expires_at INTEGER NOT NULL
    )''')
    expires_at = int(time.time()) + expires_in
    c.execute('REPLACE INTO tokens (user_id, access_token, refresh_token, expires_at) VALUES (?, ?, ?, ?)',
              (user_id, access_token, refresh_token, expires_at))
    conn.commit()
    conn.close()

def get_token(user_id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT access_token, refresh_token, expires_at FROM tokens WHERE user_id=?', (user_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    access_token, refresh_token, expires_at = row
    if expires_at < int(time.time()):
        return 'expired'
    return access_token

def refresh_access_token(user_id, refresh_func):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT refresh_token FROM tokens WHERE user_id=?', (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None
    refresh_token = row[0]
    # Call the provided refresh_func to get new tokens
    new_access_token, new_refresh_token, expires_in = refresh_func(refresh_token)
    store_token(user_id, new_access_token, new_refresh_token, expires_in)
    conn.close()
    return new_access_token
