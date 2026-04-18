import unittest
from backend.save_meal_plan_history import save_meal_plan_history
from backend.fetch_meal_plan_history import fetch_meal_plan_history
import sqlite3

class TestProfileAndHistory(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE meal_plan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            week_start DATE,
            plan_json TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        self.conn.commit()

    def test_save_and_fetch_meal_plan_history(self):
        save_meal_plan_history(1, '2025-10-05', '{"plan": "A"}')
        history = fetch_meal_plan_history(1)
        self.assertTrue(len(history) > 0)
        self.assertEqual(history[0][0], '2025-10-05')
        self.assertEqual(history[0][1], '{"plan": "A"}')

if __name__ == '__main__':
    unittest.main()
