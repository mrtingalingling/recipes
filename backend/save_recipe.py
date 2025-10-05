# T17/T18: Save recipe and link with store deals
import sqlite3

def save_recipe(user_id, title, ingredients, instructions, thumbnail, external_url=None):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT,
        thumbnail TEXT,
        external_url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''INSERT INTO recipes (user_id, title, ingredients, instructions, thumbnail, external_url) VALUES (?, ?, ?, ?, ?, ?)''',
              (user_id, title, ingredients, instructions, thumbnail, external_url))
    conn.commit()
    conn.close()

def link_recipe_with_deals(recipe_id, deal_ids):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recipe_deals (
        recipe_id INTEGER,
        deal_id INTEGER,
        PRIMARY KEY (recipe_id, deal_id)
    )''')
    for deal_id in deal_ids:
        c.execute('INSERT OR IGNORE INTO recipe_deals (recipe_id, deal_id) VALUES (?, ?)', (recipe_id, deal_id))
    conn.commit()
    conn.close()
