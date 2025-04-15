from flask import Flask, redirect, request
import requests
import base64
import urllib.parse

app = Flask(__name__)

# Spotify app credentials
CLIENT_ID = 'f598073d91714cc3bfe9df621a92279f'
CLIENT_SECRET = 'f8c23888e3314856ac6c2af59b8537e9'
REDIRECT_URI = 'https://si206final.com/udlerhod'

# Step 1: Redirect user to Spotify login
@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'
    auth_url = 'https://accounts.spotify.com/authorize'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope
    }

    return redirect(f"{auth_url}?{urllib.parse.urlencode(params)}")

# Step 2: Handle redirect from Spotify (exchange code for access token)
@app.route('/udlerhod')
def callback():
    code = request.args.get('code')

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

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')

        # You can store this token in a session or variable to use later
        return f"Access token received! <br>Access Token: {access_token}"
    else:
        return f"Failed to get token. {response.status_code}: {response.text}"

# OPTIONAL: Use access token to get user info (you'd normally pass the token here)
@app.route('/user')
def user_info():
    access_token = 'your-access-token-here'  # Replace manually for now

    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
