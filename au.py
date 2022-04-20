import json
from flask import Flask, request, redirect, g, render_template
import requests
from config import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__)

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
REDIRECT_URI = "http://127.0.0.1:8080/callback/q"
SCOPE = "playlist-modify-public playlist-modify-private"

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}


@app.route("/authenticate")
def index():
    params_list = ''
    for i, j in auth_query_parameters.items():
      params_list = params_list + i + '=' + j + '&'
    return redirect(f"{SPOTIFY_AUTH_URL}/?{params_list}")

@app.route("/callback/q")
def callback():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)
    response_data = json.loads(post_request.text)
    print(response_data)
    access_token = response_data["access_token"]
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    print(authorization_header)
    return authorization_header