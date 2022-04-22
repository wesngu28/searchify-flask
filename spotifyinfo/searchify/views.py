from flask import Blueprint, render_template, url_for, request, redirect, session, Response
from spotifyinfo.searchify.playlist import playlist_info
from spotifyinfo.searchify.artist import artist_info
from spotifyinfo.searchify.utilities import search_youtube, randomize_adjective
from spotifyinfo.searchify.track import track_info
from spotifyinfo.searchify.album import album_info
from spotifyinfo.searchify.user import user_info
import spotipy
import pandas as pd

searchify = Blueprint('searchify', __name__)

@searchify.route("/search", methods=["POST"])
@searchify.route("/home")
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
        name = general_info_flow(playlist_info, sp, link, 'info')
        return redirect(url_for("searchify.playlist", play=name))

      if 'artist' in link:
        name = general_info_flow(artist_info, sp, link, 'info')
        return redirect(url_for("searchify.artist", artist=name))

      if 'track' in link:
        name = general_info_flow(track_info, sp, link, 'info')
        return redirect(url_for("searchify.track", track=name))

      if 'album' in link:
        name = general_info_flow(album_info, sp, link, 'info')
        return redirect(url_for("searchify.album", album=name))
    except:
      return 'Error encountered'
  else:
    return render_template("home.html")

def general_info_flow(functionName, sp, link, sessiontype):
    outcome_dict = functionName(sp, link)
    session[sessiontype] = outcome_dict
    link_df = search_youtube(outcome_dict['tracks'])
    link_dict = link_df.to_dict('list')
    session['links'] = link_dict
    return outcome_dict['name']

@searchify.route("/artist/<artist>")
def artist(artist):
    dictionaries = commonRoute()
    genres = dictionaries[1]['genres']
    main_genre = genres[0]
    description = f"The {randomize_adjective()} {dictionaries[1]['name']} is a {main_genre} artist. They make {randomize_adjective()} music of {dictionaries[1]['genre_list']} genres."
    table_use = "If you like this artist, here are some songs you may like!"
    return render_template("spotify.html", table_use = table_use, play = dictionaries[1]['name'], description = description, info = dictionaries[1], column_names=dictionaries[0].columns.values, row_data=list(dictionaries[0].values.tolist()), zip=zip)

@searchify.route("/album/<album>")
def album(album):
    dictionaries = commonRoute()
    description = f"The {randomize_adjective()} {dictionaries[1]['name']} is an album by {dictionaries[1]['main_artist']}. Released on {dictionaries[1]['release_date']}, it has {randomize_adjective()} {dictionaries[1]['total_tracks']} total songs."
    table_use = "If you like this artist, here are some songs you may like!"
    return render_template("spotify.html", table_use = table_use, play = dictionaries[1]['name'], description = description, info = dictionaries[1], column_names=dictionaries[0].columns.values, row_data=list(dictionaries[0].values.tolist()), zip=zip)

@searchify.route("/user")
def user():
    try:
      sp = spotipy.Spotify(auth=session["token"])
      df = user_info(sp)
      description = f"The {randomize_adjective()} {df['name']} is you."
      if df['current_song']:
        current_song = f"You are currently listening to the {randomize_adjective()} song {df['current_song']}, by {df['current_artists']}"
      else:
        current_song = 'You are not currently listening to any song.'
      return render_template("user.html", play = df['name'], description = description, info = df, current_song = current_song, column_names=df['top_artists'].columns.values, row_data=list(df['top_artists'].values.tolist()),
                            column_names2=df['top_songs'].columns.values, row_data2=list(df['top_songs'].values.tolist()), zip=zip)
    except spotipy.exceptions.SpotifyException:
      return render_template("index.html")

@searchify.route("/track/<track>")
def track(track):
    dictionaries = commonRoute()
    description = f"The {randomize_adjective()} song {dictionaries[1]['name']} was made by the {randomize_adjective()} {dictionaries[1]['artist']}. It was released on {dictionaries[1]['release']} in the {randomize_adjective()} album {dictionaries[1]['album']}."
    table_use = "If you like this song, here are some other songs you may like!"
    return render_template("spotify.html", table_use = table_use, play = dictionaries[1]['name'], description = description, info = dictionaries[1], column_names=dictionaries[0].columns.values, row_data=list(dictionaries[0].values.tolist()), zip=zip)

@searchify.route("/playlist/<play>")
def playlist(play):
    dictionaries = commonRoute()
    description = f"{dictionaries[1]['name']} was created on {dictionaries[1]['created']}. This {randomize_adjective()} playlist has size {dictionaries[1]['size']} with the {randomize_adjective()} {dictionaries[1]['frequent']} being the most frequent, appearing {dictionaries[1]['frequent_count']}."
    table_use = "Youtube Links to the songs in this playlist"
    return render_template("spotify.html", table_use = table_use, play = dictionaries[1]['name'], description = description, info = dictionaries[1], column_names=dictionaries[0].columns.values, row_data=list(dictionaries[0].values.tolist()), zip=zip)

def commonRoute():
    if session['links']:
      link_dict = session['links']
      link_df = pd.DataFrame(link_dict)
      info_dict = session['info']
      return link_df, info_dict