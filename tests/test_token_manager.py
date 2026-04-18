import unittest
import time
from backend.token_manager import store_token, get_token, refresh_access_token

def dummy_refresh_func(refresh_token):
    # Simulate token refresh
    return ('new_access_token', 'new_refresh_token', 60)

class TestTokenManager(unittest.TestCase):
    def setUp(self):
        # Setup: store a token that expires in 1 second
        store_token(1, 'access_token', 'refresh_token', 1)

    def test_token_expiration(self):
        time.sleep(2)
        token = get_token(1)
        self.assertEqual(token, 'expired')

    def test_token_refresh(self):
        time.sleep(2)
        token = get_token(1)
        self.assertEqual(token, 'expired')
        new_token = refresh_access_token(1, dummy_refresh_func)
        self.assertEqual(new_token, 'new_access_token')
        token = get_token(1)
        self.assertEqual(token, 'new_access_token')

if __name__ == '__main__':
    unittest.main()
