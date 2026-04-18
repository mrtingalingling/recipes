# T35/T36: Retrieve past meal plans
import sqlite3

def fetch_meal_plan_history(user_id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT week_start, plan_json FROM meal_plan_history WHERE user_id=? ORDER BY week_start DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows
