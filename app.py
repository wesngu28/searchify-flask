from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session

from datetime import datetime
from playlist import getAPIKeys, playlist_to_dataframe, playlist_to_dict, get_Info
from artist import artist_recommendations, artist_info
from search import search_youtube, randomize_adjective
from track import track_info, track_recommendations
from album import album_info
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
        song_df = get_Info(sp, link, playlist_df)
        session['songs'] = song_df
        return redirect(url_for("playlist", play=song_df['name']))

      if 'artist' in link:
        artist_dict = artist_info(sp, link)
        session['artist'] = artist_dict
        song_list = artist_recommendations(sp, link)
        link_df = search_youtube(song_list)
        link_dict = link_df.to_dict('list')
        session['links'] = link_dict
        return redirect(url_for("artist", artist=artist_dict['name']))

      if 'track' in link:
        track_dict = track_info(sp, link)
        session['track'] = track_dict
        song_list = track_recommendations(sp, link)
        link_df = search_youtube(song_list)
        link_dict = link_df.to_dict('list')
        session['links'] = link_dict
        return redirect(url_for("track", track=track_dict['name']))
      if 'album' in link:
        album_dict = album_info(sp, link)
        session['album'] = album_dict
        print(album_dict)
        link_df = search_youtube(album_dict['tracks'])
        link_dict = link_df.to_dict('list')
        session['links'] = link_dict
        return redirect(url_for("album", album=album_dict['name']))
    except:
      return "Issue encountered"
  else:
    return render_template("index.html")

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

@app.route("/user/<user>")
def user(user):
  print('oks!')
  return render_template("index.html")

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
    song_df = session['songs']
    if play != song_df['name']:
      return render_template("index.html")
    description = f"{play} was created on {song_df['created']}. This {randomize_adjective()} playlist has size {song_df['size']} with the {randomize_adjective()} {song_df['frequent']} being the most frequent, appearing {song_df['frequent_count']}."
    table_use = "Youtube Links to the songs in this playlist"
    return render_template("spotify.html", table_use = table_use, play = play, description = description, info = song_df, column_names=link_df.columns.values, row_data=list(link_df.values.tolist()),
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

if __name__ == "__main__":
  app.run(debug=True)