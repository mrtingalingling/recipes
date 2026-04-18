import unittest
from backend.generate_shopping_list import generate_shopping_list
from backend.export_shopping_list import export_to_csv, export_to_pdf
import os

class TestShoppingList(unittest.TestCase):
    def test_generate_shopping_list(self):
        meal_plan = [
            {'ingredients': [{'name': 'Egg', 'store': 'StoreA'}, {'name': 'Milk', 'store': 'StoreB'}]},
            {'ingredients': [{'name': 'Bread', 'store': 'StoreA'}]}
        ]
        items = generate_shopping_list(1, '2025-10-05', meal_plan)
        self.assertIn('StoreA', items)
        self.assertIn('StoreB', items)
        self.assertIn('Egg', items['StoreA'])
        self.assertIn('Milk', items['StoreB'])

    def test_export_to_csv(self):
        list_json = '{"StoreA": ["Egg", "Bread"], "StoreB": ["Milk"]}'
        export_to_csv(list_json, 'test_list.csv')
        self.assertTrue(os.path.exists('test_list.csv'))
        os.remove('test_list.csv')

    def test_export_to_pdf(self):
        list_json = '{"StoreA": ["Egg", "Bread"], "StoreB": ["Milk"]}'
        export_to_pdf(list_json, 'test_list.pdf')
        self.assertTrue(os.path.exists('test_list.pdf'))
        os.remove('test_list.pdf')

if __name__ == '__main__':
    unittest.main()
