import unittest
from backend.scrape_store_ads import scrape_store_ads

class DummyAIApiFunc:
    def __init__(self):
        self.token_refreshed = False
    def scrape(self, token):
        return [{'store_name': 'StoreA', 'product_name': 'Milk', 'price': 2.99, 'validity_start': '2025-10-01', 'validity_end': '2025-10-07', 'geo_location': '40.7128,-74.0060'}]
    def refresh(self, refresh_token):
        self.token_refreshed = True
        return ('new_token', 'new_refresh', 60)

class TestScrapeStoreAds(unittest.TestCase):
    def test_scrape_with_valid_token(self):
        # Setup: Assume token_manager returns valid token
        import backend.token_manager
        backend.token_manager.get_token = lambda user_id: 'valid_token'
        api = DummyAIApiFunc()
        ads = scrape_store_ads(1, api)
        self.assertTrue(len(ads) > 0)

    def test_scrape_with_expired_token(self):
        import backend.token_manager
        backend.token_manager.get_token = lambda user_id: 'expired'
        backend.token_manager.refresh_access_token = lambda user_id, func: 'new_token'
        api = DummyAIApiFunc()
        ads = scrape_store_ads(1, api)
        self.assertTrue(api.token_refreshed)
        self.assertTrue(len(ads) > 0)

if __name__ == '__main__':
    unittest.main()
