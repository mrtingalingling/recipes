# T40: Track metrics
import sqlite3

def track_metric(event, user_id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT,
        user_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('INSERT INTO analytics (event, user_id) VALUES (?, ?)', (event, user_id))
    conn.commit()
    conn.close()
