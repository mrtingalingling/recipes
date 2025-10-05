import unittest
from backend.generate_meal_plan import generate_meal_plan
from backend.fetch_meal_plan import fetch_meal_plan
import sqlite3

class TestMealPlan(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            week_start DATE,
            plan_json TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        self.conn.commit()

    def test_generate_and_fetch_meal_plan(self):
        recipes = [
            {'title': 'A', 'ingredients': 'vegan', 'cost': 10},
            {'title': 'B', 'ingredients': 'vegan', 'cost': 15},
            {'title': 'C', 'ingredients': 'vegan', 'cost': 5}
        ]
        selected = generate_meal_plan(1, 30, 'vegan', [], recipes)
        self.assertTrue(len(selected) > 0)
        plan = fetch_meal_plan(1)
        self.assertEqual(plan[0]['title'], 'A')

if __name__ == '__main__':
    unittest.main()
