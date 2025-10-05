# Secure authentication and authorization for AI API
import requests
from backend.token_manager import store_token

def authenticate_ai_api(user_id, username, password):
    # Example: POST to AI API auth endpoint
    response = requests.post('https://aiapi.example.com/auth', json={
        'username': username,
        'password': password
    })
    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token']
        refresh_token = data.get('refresh_token')
        expires_in = data['expires_in']
        store_token(user_id, access_token, refresh_token, expires_in)
        return True
    return False
