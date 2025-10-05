import unittest
from backend.analytics import track_metric
import sqlite3

class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        self.conn.commit()

    def test_track_metric(self):
        track_metric('budget_plan_created', 1)
        self.c.execute('SELECT event, user_id FROM analytics')
        row = self.c.fetchone()
        self.assertEqual(row[0], 'budget_plan_created')
        self.assertEqual(row[1], 1)

if __name__ == '__main__':
    unittest.main()
