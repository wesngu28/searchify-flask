from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from playlistmanipulate import playlist_to_dataframe, playlist_to_dict, get_Info
from search import search_youtube
import os
import pandas as pd
import pathlib
from dotenv import load_dotenv

fileLocation = pathlib.Path(__file__).parent.resolve()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///playlist.db"
db = SQLAlchemy(app)

class PlaylistTable(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), default=0)
  link = db.Column(db.String(80), default=0, unique=True)
  date_added = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return "<Playlist %r" % self.id

@app.route("/", methods=["POST", "GET"])
def index():
  load_dotenv()
  env_cid = os.getenv("CID")
  env_sid = os.getenv("SID")
  if request.method == "POST":
    if request.form["cid"]:
      user_cid = request.form["cid"]
    elif env_cid != "YOUR CID HERE" or env_cid != "":
      user_cid = env_cid
    else:
      return "Please provide a client ID"
    if request.form["cid"]:
      user_sid = request.form["sid"]
    elif env_sid != "YOUR SID HERE" or env_sid != "":
      user_sid = env_sid
    else:
      return "Please provide a secret ID"
    client_credentials_manager = SpotifyClientCredentials(client_id=user_cid,client_secret=user_sid)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    if request.form["pl"]:
      playlist_link = request.form["pl"]
    else:
      return "Please provide a Spotify link"

    try:
      playlist_df = playlist_to_dataframe(sp, playlist_link)
      song_list = playlist_to_dict(sp, playlist_link)
      link_df = search_youtube(song_list)
      link_dict = link_df.to_dict('list')
      session['links'] = link_dict
      song_df = get_Info(sp, playlist_link, link_df, playlist_df)
      song_dict = song_df.to_dict('list')
      session['songs'] = song_dict
      output_csv = song_df['name'].iloc[0] + ".csv"
      link_df.to_csv(output_csv, index=False)
      print("File saved to: {} with name {}".format(str(fileLocation),output_csv))
      new_playlist = PlaylistTable(name = song_df['name'].iloc[0], link = playlist_link)
      db.session.add(new_playlist)
      db.session.commit()
      return redirect(url_for("playlist", play=song_df['name'].iloc[0]))
    except:
      return "Issue encountered"
  else:
    playlists = PlaylistTable.query.order_by(PlaylistTable.date_added.desc()).limit(10)
    return render_template("index.html", playlists=playlists)

@app.route("/<play>")
def playlist(play):
  if session['links'] in session:
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    song_dict = session['songs']
    song_df = pd.DataFrame(song_dict)
    return render_template("playlist.html", play = play, song_info = song_df, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
                           link_column="Playlist Name", zip=zip)

if __name__ == "__main__":
  app.run(debug=True)