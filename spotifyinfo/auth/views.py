from flask import Blueprint, url_for, request, redirect, session, render_template
from spotifyinfo.config import SPOTIFY_AUTH_URL, SPOTIFY_TOKEN_URL, REDIRECT_URI, CLIENT_ID, CLIENT_SECRET, AUTH_QUERY_PARAMETERS
from pathlib import Path
import requests
import pandas as pd
import json

auth = Blueprint('auth', __name__)

#Authorization flow begins when the page is loaded, prompting user access in order to procure a token for access
@auth.route("/", methods=["GET", "POST"])
def home():
    params_list = ''
    for i, j in AUTH_QUERY_PARAMETERS.items():
      params_list = params_list + i + '=' + j + '&'
    params_list = params_list[:-1]
    return redirect(f"{SPOTIFY_AUTH_URL}/?{params_list}")
@auth.route("/callback/")
def callback():
    session.clear()
    try:
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
      access_token = response_data["access_token"]
      session['token'] = access_token
      return redirect(url_for("searchify.index"))
    except:
      return redirect(url_for("auth.home"))

#Function that creates a download folder in the directory and downloads CSVs to it
fileLocation = Path(__file__).parent
@auth.route('/download-csv')
def downloadCSV():
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    info_dict = session['info']
    output_csv = info_dict['name'] + ".csv"
    dl = Path('downloads')
    dl.mkdir(parents=True,exist_ok=True)
    link_df.to_csv('downloads/' + output_csv, index=False)
    return f"File saved to: {str(fileLocation)} with name {output_csv}"