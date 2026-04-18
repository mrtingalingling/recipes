# T4: Save/Update user preferences in SQLite
import sqlite3

def save_user_preferences(budget, household_size, dietary_preferences, cooking_time):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        budget REAL NOT NULL,
        household_size INTEGER NOT NULL,
        dietary_preferences TEXT,
        cooking_time INTEGER NOT NULL
    )''')
    c.execute('SELECT id FROM user_profile LIMIT 1')
    row = c.fetchone()
    if row:
        c.execute('''UPDATE user_profile SET budget=?, household_size=?, dietary_preferences=?, cooking_time=? WHERE id=?''',
                  (budget, household_size, dietary_preferences, cooking_time, row[0]))
    else:
        c.execute('''INSERT INTO user_profile (budget, household_size, dietary_preferences, cooking_time) VALUES (?, ?, ?, ?)''',
                  (budget, household_size, dietary_preferences, cooking_time))
    conn.commit()
    conn.close()
