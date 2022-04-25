import os

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"
REDIRECT_URI = "http://127.0.0.1:5000/callback/"
SCOPE = "user-top-read user-read-currently-playing"
CLIENT_ID = 'Enter Client ID'
CLIENT_SECRET = 'Enter Secret ID'
AUTH_QUERY_PARAMETERS = {
  "response_type": "code",
  "redirect_uri": REDIRECT_URI,
  "scope": SCOPE,
  "client_id": CLIENT_ID,
}