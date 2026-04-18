import unittest
from backend.save_user_preferences import save_user_preferences
from backend.save_recipe import save_recipe
from backend.generate_meal_plan import generate_meal_plan
from backend.generate_shopping_list import generate_shopping_list

class TestEndToEnd(unittest.TestCase):
    def test_full_flow(self):
        # Budget → Deals → Recipes → Plan → List → Export
        save_user_preferences(100, 2, 'vegan', 45)
        save_recipe(1, 'Vegan Pancakes', 'Flour, Soy Milk', 'Mix and cook.', 'img.jpg')
        recipes = [{'title': 'Vegan Pancakes', 'ingredients': 'vegan', 'cost': 10}]
        meal_plan = generate_meal_plan(1, 100, 'vegan', [], recipes)
        shopping_list = generate_shopping_list(1, '2025-10-05', meal_plan)
        self.assertIn('Vegan Pancakes', [r['title'] for r in meal_plan])
        self.assertIn('Soy Milk', shopping_list.get('Unknown', []))

if __name__ == '__main__':
    unittest.main()
