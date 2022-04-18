from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session

from datetime import datetime
from playlistmanipulate import getAPIKeys, playlist_to_dataframe, playlist_to_dict, get_Info
from search import search_youtube
import pandas as pd
import pathlib

fileLocation = pathlib.Path(__file__).parent.resolve()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["POST", "GET"])
def index():
  if request.method == "POST":
    if request.form["pl"]:
      playlist_link = request.form["pl"]
    else:
      return render_template("index.html", error_msg = 'Provide a Playlist Link')
    sp = getAPIKeys()
    if sp is None:
      return render_template("index.html", error_msg = 'Provide your IDs in the environment file')
    try:
      session.clear()
      playlist_df = playlist_to_dataframe(sp, playlist_link)
      song_list = playlist_to_dict(sp, playlist_df)
      link_df = search_youtube(song_list)
      link_dict = link_df.to_dict('list')
      session['links'] = link_dict
      song_df = get_Info(sp, playlist_link, link_df, playlist_df)
      print(song_df)
      song_dict = song_df.to_dict('list')
      session['songs'] = song_dict
      output_csv = song_df['name'].iloc[0] + ".csv"
      link_df.to_csv('playlists/' + output_csv, index=False)
      print("File saved to: {} with name {}".format(str(fileLocation),output_csv))
      return redirect(url_for("playlist", play=song_df['name'].iloc[0]))
    except:
      return "Issue encountered"
  else:
    return render_template("index.html")

@app.route("/playlist/<play>")
def playlist(play):
  if session['links']:
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    song_dict = session['songs']
    song_df = pd.DataFrame(song_dict)
    return render_template("playlist.html", play = play, song_info = song_df, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
                           link_column="Playlist Name", zip=zip)

if __name__ == "__main__":
  app.run(debug=True)