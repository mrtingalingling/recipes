# T38: OAuth login (Google, Apple, Email)
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='GOOGLE_CLIENT_ID',
    client_secret='GOOGLE_CLIENT_SECRET',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def authorize_google():
    token = google.authorize_access_token()
    user = google.get('userinfo').json()
    session['user'] = user
    return redirect('/')

# Similar setup for Apple and Email
