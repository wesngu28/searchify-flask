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

    playlist_tracks_artist = []
    playlist_tracks_titles = []
    for track in tracks:
        if(track['track']['id']!=None):
            playlist_tracks_titles.append(track['track']['name'])
            playlist_tracks_artist.append(track['track']['artists'][0]['name'])

    list = dict(zip(playlist_tracks_titles, playlist_tracks_artist))
    return list

def get_Info(sp, URL, df, df2):

    cover_url = sp.playlist_cover_image(URL)
    cover_url = cover_url[0]['url']

    playlist_name = sp.playlist(URL, fields="name")
    playlist_name = playlist_name['name']

    playlist_creation = df2['items'][0]['added_at']
    playlist_creation = playlist_creation[0:10]

    playlist_size = df2['total']

    mode = df['Artist'].value_counts().idxmax()
    item_counts = df['Artist'].value_counts()
    max_item = item_counts.max()

    quickInfo = pd.DataFrame()
    quickInfo['img'] = [cover_url]
    quickInfo['name'] = [playlist_name]
    quickInfo['size'] = [playlist_size]
    quickInfo['created'] = [playlist_creation]
    quickInfo['frequent'] = [mode]
    quickInfo['frequent_count'] = [str(max_item)]
    print(sp.current_playback)
    return quickInfo