import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import importlib
import os
import pandas as pd

def getAPIKeys():
    load_dotenv()
    env_cid = os.getenv("CID")
    env_sid = os.getenv("SID")
    if env_cid and env_sid:
      client_credentials_manager = SpotifyClientCredentials(client_id=env_cid,client_secret=env_sid)
      sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
      return sp
    return

def playlist_to_dataframe(sp, URL):
    playlist_tracks_df= sp.playlist_tracks(URL)
    return playlist_tracks_df

def playlist_to_dict(sp, df):
    tracks = df['items']
    while df['next']:
        df = sp.next(df)
        tracks.extend(df['items'])

    playlist_tracks_titles = []
    for track in tracks:
        if(track['track']['id']!=None):
            playlist_tracks_titles.append(track['track']['name'])

    playlist_tracks_artist = []
    for artist in tracks:
        if (len(artist['track']['artists']) > 1):
            artist_counter = 0
            artist_list = ''
            while (len(artist['track']['artists']) > artist_counter):
                artist_list = artist_list + artist['track']['artists'][artist_counter]['name'] + ', '
                artist_counter = artist_counter + 1
            artist_list = artist_list[:-2]
            playlist_tracks_artist.append(artist_list)
        else:
            playlist_tracks_artist.append(artist['track']['artists'][0]['name'])
    list = dict(zip(playlist_tracks_titles, playlist_tracks_artist))
    return list

def get_Info(sp, URL, df):

    cover_url = sp.playlist_cover_image(URL)
    cover_url = cover_url[0]['url']

    playlist_name = sp.playlist(URL, fields="name")
    playlist_name = playlist_name['name']

    playlist_creation = df['items'][0]['added_at']
    playlist_creation = playlist_creation[0:10]

    playlist_size = df['total']

    tracks = df['items']
    playlist_tracks_artist = []
    for track in tracks:
        if(track['track']['id']!=None):
            playlist_tracks_artist.append(track['track']['artists'][0]['name'])
    count_df = pd.DataFrame({'Number': playlist_tracks_artist})

    mode = count_df.value_counts().idxmax()
    item_counts = count_df.value_counts()
    max_item = item_counts.max()
    if(max_item == 1):
        max_item = 'once'
    else:
        max_item = f"{max_item} times"

    playlist = {
        "name": playlist_name,
        "size": playlist_size,
        "created": playlist_creation,
        "frequent": mode[0],
        "frequent_count": str(max_item),
        "img": cover_url
    }
    return playlist