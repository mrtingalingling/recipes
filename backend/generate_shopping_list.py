# T27: Shopping list generation logic
import sqlite3, json

def generate_shopping_list(user_id, week_start, meal_plan):
    # Flatten ingredients from meal plan
    items = {}
    for meal in meal_plan:
        for ingredient in meal.get('ingredients', []):
            store = ingredient.get('store', 'Unknown')
            if store not in items:
                items[store] = []
            items[store].append(ingredient['name'])
    list_json = json.dumps(items)
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS shopping_lists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        week_start DATE,
        list_json TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''INSERT INTO shopping_lists (user_id, week_start, list_json) VALUES (?, ?, ?)''',
              (user_id, week_start, list_json))
    conn.commit()
    conn.close()
    return items
