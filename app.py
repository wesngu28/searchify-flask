from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session

from datetime import datetime
from playlist import getAPIKeys, playlist_to_dataframe, playlist_to_dict, get_Info
from artist import artist_recommendations, artist_info
from search import search_youtube, randomize_adjective
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
    if request.form["inp"]:
      link = request.form["inp"]
    else:
      return render_template("index.html", error_msg = 'Provide a Playlist Link')
    sp = getAPIKeys()
    if sp is None:
      return render_template("index.html", error_msg = 'Provide your IDs in the environment file')
    try:
      session.clear()
      link = request.form["inp"]
      if 'playlist' in link:
        playlist_df = playlist_to_dataframe(sp, link)
        song_list = playlist_to_dict(sp, playlist_df)
        link_df = search_youtube(song_list)
        link_dict = link_df.to_dict('list')
        session['links'] = link_dict
        song_df = get_Info(sp, link, link_df, playlist_df)
        print(song_df)
        song_dict = song_df.to_dict('list')
        session['songs'] = song_dict
        return redirect(url_for("playlist", play=song_df['name'].iloc[0]))
      if 'artist' in link:
        artist_df = artist_info(sp, link)
        artist_dict = artist_df.to_dict('list')
        session['artist'] = artist_dict
        song_list = artist_recommendations(sp, link)
        link_df = search_youtube(song_list)
        link_dict = link_df.to_dict('list')
        session['links'] = link_dict
        return redirect(url_for("artist", artist=artist_df['name'].iloc[0]))
      if 'track' in link:
        track_link = link
    except:
      return "Issue encountered"
  else:
    return render_template("index.html")

@app.route("/artist/<artist>")
def artist(artist):
  if session['links']:
    artist_dict = session['artist']
    artist_df = pd.DataFrame(artist_dict)
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    genres = artist_df['genres'].iloc[0]
    main_genre = genres[0]
    description = f"The {randomize_adjective()} {artist} is a {main_genre} artist. They make {randomize_adjective()} music of {artist_df['genre_list'].iloc[0]} genres, according to Spotify."
  return render_template("artist.html", description = description, artist_df = artist_df, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
                           link_column="coffee", zip=zip)

@app.route("/album/<album>")
def album(album):
  print('oks!')
  return render_template("index.html")

@app.route("/user/<user>")
def user(user):
  print('oks!')
  return render_template("index.html")

@app.route("/track/<track>")
def track(track):
  if session['links']:
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    song_dict = session['songs']
    song_df = pd.DataFrame(song_dict)
    if play != song_df['name'].iloc[0]:
      return render_template("index.html")
    description = f"{play} was created on {song_df['created'].iloc[0]}. This {randomize_adjective()} playlist has size {song_df['size'].iloc[0]} with the {randomize_adjective()} {song_df['frequent'].iloc[0]} being the most frequent, appearing {song_df['frequent_count'].iloc[0]}."
    print(description)
    return render_template("playlist.html", play = play, description = description, song_info = song_df, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
                           link_column="Playlist Name", zip=zip)

@app.route("/playlist/<play>")
def playlist(play):
  if session['links']:
    link_dict = session['links']
    link_df = pd.DataFrame(link_dict)
    song_dict = session['songs']
    song_df = pd.DataFrame(song_dict)
    if play != song_df['name'].iloc[0]:
      return render_template("index.html")
    description = f"{play} was created on {song_df['created'].iloc[0]}. This {randomize_adjective()} playlist has size {song_df['size'].iloc[0]} with the {randomize_adjective()} {song_df['frequent'].iloc[0]} being the most frequent, appearing {song_df['frequent_count'].iloc[0]}."
    print(description)
    return render_template("playlist.html", play = play, description = description, song_info = song_df, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
                           link_column="Playlist Name", zip=zip)

@app.route('/download-csv')
def downloadCSV():
  link_dict = session['links']
  link_df = pd.DataFrame(link_dict)
  print(link_df)
  song_dict = session['songs']
  song_df = pd.DataFrame(song_dict)
  output_csv = song_df['name'].iloc[0] + ".csv"
  link_df.to_csv('playlists/' + output_csv, index=False)
  return f"File saved to: {str(fileLocation)} with name {output_csv}"

if __name__ == "__main__":
  app.run(debug=True)