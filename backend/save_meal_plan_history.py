# T35: Storage of past meal plans
import sqlite3

def save_meal_plan_history(user_id, week_start, plan_json):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS meal_plan_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        week_start DATE,
        plan_json TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''INSERT INTO meal_plan_history (user_id, week_start, plan_json) VALUES (?, ?, ?)''',
              (user_id, week_start, plan_json))
    conn.commit()
    conn.close()
