from flask import Flask, request, redirect
import requests
import base64
import urllib.parse
import os

app = Flask(__name__)

# Replace these with your Spotify app credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:5000/callback'

# Authorization URL and Token URL
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

@app.route('/')
def index():
    return '<a href="/login">Log in with Spotify</a>'

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'
    state = 'some_random_state'  # You can make this dynamic for security

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope,
        'state': state
    }

    url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')

    if state != 'some_random_state':
        return 'State mismatch. Possible CSRF attack.'

    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    token_info = response.json()

    return token_info  # Shows access_token, refresh_token, etc.

if __name__ == '__main__':
    app.run(debug=True)
