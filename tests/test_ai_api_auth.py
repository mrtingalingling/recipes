import unittest
from unittest.mock import patch
from backend.ai_api_auth import authenticate_ai_api

class TestAIApiAuth(unittest.TestCase):
    @patch('backend.ai_api_auth.requests.post')
    def test_authenticate_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'access_token': 'token',
            'refresh_token': 'refresh',
            'expires_in': 60
        }
        result = authenticate_ai_api(1, 'user', 'pass')
        self.assertTrue(result)

    @patch('backend.ai_api_auth.requests.post')
    def test_authenticate_failure(self, mock_post):
        mock_post.return_value.status_code = 401
        result = authenticate_ai_api(1, 'user', 'wrongpass')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
