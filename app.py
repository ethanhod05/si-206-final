from flask import Flask, redirect, request
import requests
import base64
import urllib.parse

app = Flask(__name__)

# Replace with your Spotify app credentials
CLIENT_ID = '62df1bd7a8b641d899cf46a72d9e8195'
CLIENT_SECRET = '98254d2479944fed9ac4c4d2281e8de7'
REDIRECT_URI = 'https://si206final.com/udlerhod'

# Step 1: Authorization Request (User logs in)
@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'  # Scopes you're requesting
    auth_url = 'https://accounts.spotify.com/authorize'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': scope
    }

    # Redirect to Spotify's authorization page
    return redirect(f"{auth_url}?{urllib.parse.urlencode(params)}")

# Step 2: Handle the Redirect (Exchange authorization code for an access token)
@app.route('/udlerhod')
def callback():
    # Get the code from the callback URL
    code = request.args.get('code')

    # Basic Authorization header for client authentication
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

    # Step 3: Request the access token
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    token_data = response.json()

    # Show the access token, refresh token, and other info
    return token_data  # For debugging, you can log or use the token for further requests

# Step 4: Use the access token to make a request to the Spotify API (example: get user info)
@app.route('/user')
def user_info():
    # Replace with the actual access token from the response
    access_token = 'your-access-token-here'

    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    # Example: Get the current user's profile
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_info = response.json()

    return user_info  # Shows user information like name, email, etc.

if __name__ == '__main__':
    app.run(debug=True, port=8080)
