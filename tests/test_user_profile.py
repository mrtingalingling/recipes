import unittest
import sqlite3
from backend.save_user_preferences import save_user_preferences

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            budget REAL NOT NULL,
            household_size INTEGER NOT NULL,
            dietary_preferences TEXT,
            cooking_time INTEGER NOT NULL
        )''')
        self.conn.commit()

    def test_save_new_profile(self):
        save_user_preferences(100, 2, 'vegan', 45)
        self.c.execute('SELECT * FROM user_profile')
        row = self.c.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], 100)
        self.assertEqual(row[2], 2)
        self.assertEqual(row[3], 'vegan')
        self.assertEqual(row[4], 45)

    def test_update_profile(self):
        save_user_preferences(100, 2, 'vegan', 45)
        save_user_preferences(150, 3, 'vegetarian', 30)
        self.c.execute('SELECT * FROM user_profile')
        row = self.c.fetchone()
        self.assertEqual(row[1], 150)
        self.assertEqual(row[2], 3)
        self.assertEqual(row[3], 'vegetarian')
        self.assertEqual(row[4], 30)

if __name__ == '__main__':
    unittest.main()
