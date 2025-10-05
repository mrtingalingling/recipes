# T22: Endpoint to retrieve generated meal plan
import sqlite3

def fetch_meal_plan(user_id, week_start=None):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    query = 'SELECT plan_json FROM meal_plans WHERE user_id=?'
    params = [user_id]
    if week_start:
        query += ' AND week_start=?'
        params.append(week_start)
    c.execute(query, params)
    row = c.fetchone()
    conn.close()
    if row:
        import json
        return json.loads(row[0])
    return None
