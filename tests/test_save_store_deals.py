import unittest
import sqlite3
from backend.save_store_deals import save_store_deals

class TestSaveStoreDeals(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE store_deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            validity_start DATE,
            validity_end DATE,
            geo_location TEXT
        )''')
        self.conn.commit()

    def test_save_deal(self):
        deals = [{
            'store_name': 'StoreA',
            'product_name': 'Milk',
            'price': 2.99,
            'validity_start': '2025-10-01',
            'validity_end': '2025-10-07',
            'geo_location': '40.7128,-74.0060'
        }]
        save_store_deals(deals)
        self.c.execute('SELECT * FROM store_deals')
        row = self.c.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], 'StoreA')
        self.assertEqual(row[2], 'Milk')
        self.assertEqual(row[3], 2.99)
        self.assertEqual(row[4], '2025-10-01')
        self.assertEqual(row[5], '2025-10-07')
        self.assertEqual(row[6], '40.7128,-74.0060')

if __name__ == '__main__':
    unittest.main()
