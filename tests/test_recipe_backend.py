import unittest
from backend.save_recipe import save_recipe, link_recipe_with_deals
from backend.fetch_recipes import fetch_recipes
import sqlite3

class TestRecipeBackend(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT,
            thumbnail TEXT,
            external_url TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        self.c.execute('''CREATE TABLE recipe_deals (
            recipe_id INTEGER,
            deal_id INTEGER,
            PRIMARY KEY (recipe_id, deal_id)
        )''')
        self.conn.commit()

    def test_save_and_fetch_recipe(self):
        save_recipe(1, 'Test Recipe', 'Eggs, Milk', 'Mix and cook.', 'img.jpg')
        recipes = fetch_recipes('new')
        self.assertTrue(any('Test Recipe' in r for r in recipes))

    def test_link_recipe_with_deals(self):
        save_recipe(1, 'Test Recipe', 'Eggs, Milk', 'Mix and cook.', 'img.jpg')
        self.c.execute('SELECT id FROM recipes LIMIT 1')
        recipe_id = self.c.fetchone()[0]
        link_recipe_with_deals(recipe_id, [1,2])
        self.c.execute('SELECT * FROM recipe_deals WHERE recipe_id=?', (recipe_id,))
        links = self.c.fetchall()
        self.assertEqual(len(links), 2)

if __name__ == '__main__':
    unittest.main()
