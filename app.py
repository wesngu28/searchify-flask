from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session

from datetime import datetime
from playlist import playlist_info
from artist import artist_info
from search import search_youtube, randomize_adjective
from track import track_info
from album import album_info
from user import user_info
import pandas as pd
import pathlib

fileLocation = pathlib.Path(__file__).parent.resolve()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
REDIRECT_URI = "http://127.0.0.1:5000/callback/q"
SCOPE = "user-top-read"

from dotenv import load_dotenv
import requests
import json
import os
import random
import string
import spotipy
from spotipy import oauth2
from spotipy.oauth2 import SpotifyOAuth
CLIENT_ID = os.getenv("CID")
CLIENT_SECRET = os.getenv("SID")

@app.route("/", methods=["GET", "POST"])
def home():
    state = ''.join(random.choices(string.ascii_letters, k=16))
    auth_query_parameters = {
      "response_type": "code",
      "redirect_uri": REDIRECT_URI,
      "scope": SCOPE,
      "client_id": CLIENT_ID,
      "state" : state
    }
    params_list = ''
    for i, j in auth_query_parameters.items():
      params_list = params_list + i + '=' + j + '&'
    params_list = params_list[:-1]
    return redirect(f"{SPOTIFY_AUTH_URL}/?{params_list}")

@app.route("/callback/q")
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
      print(response_data)
      access_token = response_data["access_token"]
      #authorization_header = {"Authorization": "Bearer {}".format(access_token)}
      session['token'] = access_token
      return redirect(url_for("index"))
    except:
      return redirect(url_for("home"))

@app.route("/search", methods=["POST"])
@app.route("/home")
def index():
  if request.method == "POST":
    if request.form["inp"]:
      link = request.form["inp"]
    else:
      return render_template("home.html", error_msg = 'Provide a Playlist Link')
    sp = spotipy.Spotify(auth=session["token"])
    try:
      link = request.form["inp"]
      if 'playlist' in link:
        name = general_info_flow(playlist_info, sp, link, 'playlist')
        return redirect(url_for("playlist", play=name))

      if 'artist' in link:
        name = general_info_flow(artist_info, sp, link, 'artist')
        return redirect(url_for("artist", artist=name))

      if 'track' in link:
        name = general_info_flow(track_info, sp, link, 'track')
        return redirect(url_for("track", track=name))

      if 'album' in link:
        name = general_info_flow(album_info, sp, link, 'album')
        return redirect(url_for("album", album=name))

    except:
      return "Issue encountered"
  else:
    return render_template("home.html")

def general_info_flow(functionName, sp, link, sessiontype):
    outcome_dict = functionName(sp, link)
    session[sessiontype] = outcome_dict
    link_df = search_youtube(outcome_dict['tracks'])
    link_dict = link_df.to_dict('list')
    session['links'] = link_dict
    return outcome_dict['name']

@app.route("/artist/<artist>")
def artist(artist):
  if session['links']:
    artist_dict = session['artist']
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    genres = artist_dict['genres']
    main_genre = genres[0]
    description = f"The {randomize_adjective()} {artist} is a {main_genre} artist. They make {randomize_adjective()} music of {artist_dict['genre_list']} genres."
    table_use = "If you like this artist, here are some songs you may like!"
    return render_template("spotify.html", table_use = table_use, description = description, info = artist_dict, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
                           link_column="coffee", zip=zip)

@app.route("/album/<album>")
def album(album):
  if session['links']:
    album_dict = session['album']
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    description = f"The {randomize_adjective()} {album} is an album by {album_dict['main_artist']}. Released on {album_dict['release_date']}, it has {randomize_adjective()} {album_dict['total_tracks']} total songs."
    table_use = "If you like this artist, here are some songs you may like!"
    return render_template("spotify.html", table_use = table_use, description = description, info = album_dict, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
                           link_column="coffee", zip=zip)

@app.route("/user/")
def user():
    sp = spotipy.Spotify(auth=session["token"])
    df = user_info(sp)
    print(df)
    return render_template("spotify.html")

@app.route("/track/<track>")
def track(track):
  if session['links']:
    track_dict = session['track']
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    description = f"The {randomize_adjective()} song {track} was made by the {randomize_adjective()} {track_dict['artist']}. It was released on {track_dict['release']} in the {randomize_adjective()} album {track_dict['album']}."
    print(description)
    table_use = "If you like this song, here are some other songs you may like!"
    return render_template("spotify.html", table_use = table_use, description = description, info = track_dict, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
                           link_column="coffee", zip=zip)

@app.route("/playlist/<play>")
def playlist(play):
  if session['links']:
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    playlist_dict = session['playlist']
    if play != playlist_dict['name']:
      return render_template("index.html")
    description = f"{play} was created on {playlist_dict['created']}. This {randomize_adjective()} playlist has size {playlist_dict['size']} with the {randomize_adjective()} {playlist_dict['frequent']} being the most frequent, appearing {playlist_dict['frequent_count']}."
    table_use = "Youtube Links to the songs in this playlist"
    return render_template("spotify.html", table_use = table_use, play = play, description = description, info = playlist_dict, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
                           link_column="Playlist Name", zip=zip)

@app.route('/download-csv')
def downloadCSV():
  link_dict = session['links']
  link_df = pd.DataFrame(link_dict)
  print(link_df)
  song_dict = session['songs']
  output_csv = song_dict['name'] + ".csv"
  link_df.to_csv('playlists/' + output_csv, index=False)
  return f"File saved to: {str(fileLocation)} with name {output_csv}"

@app.errorhandler(404)
def error_404(_):
    return render_template("index.html")

@app.errorhandler(405)
def error_405(_):
    return render_template("index.html")

@app.errorhandler(500)
def error_500(_):
    return render_template("index.html")

if __name__ == "__main__":
  app.run(debug=True)