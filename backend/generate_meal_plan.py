# T21: Meal plan generation algorithm
import sqlite3, json, datetime

def generate_meal_plan(user_id, budget, preferences, deals, recipes):
    # Dummy logic: select recipes within budget, matching preferences
    selected = []
    total_cost = 0
    for recipe in recipes:
        if preferences in recipe['ingredients'] and total_cost + recipe['cost'] <= budget:
            selected.append(recipe)
            total_cost += recipe['cost']
        if len(selected) == 7:
            break
    week_start = datetime.date.today().isoformat()
    plan_json = json.dumps(selected)
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS meal_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        week_start DATE,
        plan_json TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''INSERT INTO meal_plans (user_id, week_start, plan_json) VALUES (?, ?, ?)''',
              (user_id, week_start, plan_json))
    conn.commit()
    conn.close()
    return selected
