# T19: API for fetching recipe lists with filters
import sqlite3

def fetch_recipes(filter_type='new'):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    query = 'SELECT * FROM recipes ORDER BY created_at DESC'
    if filter_type == 'healthiest':
        query = 'SELECT * FROM recipes WHERE instructions LIKE "%healthy%" ORDER BY created_at DESC'
    elif filter_type == 'popular':
        query = 'SELECT * FROM recipes ORDER BY id DESC LIMIT 10'  # Example popularity
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows
