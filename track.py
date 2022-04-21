import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

def track_info(sp, url):
    df = sp.track(url)
    artists = ''
    for information in df['artists']:
      artists = artists + information['name'] + ', '
    artists = artists[:-2]

    url = [url]
    rec_df = sp.recommendations(seed_tracks=url, limit=10)
    rec_df = rec_df['tracks']
    recommended_track = []
    recommended_artists = []
    for recommendation in rec_df:
        recommended_track.append(recommendation['name'])
        if(len(recommendation['artists']) > 1):
            artist_count = 0
            artist = ''
            while(artist_count < len(recommendation['artists'])):
                artist = artist + recommendation['artists'][artist_count]['name'] + ', '
                artist_count = artist_count + 1
            artist = artist[:-2]
            recommended_artists.append(artist)
        else:
            recommended_artists.append(recommendation['artists'][0]['name'])
    list = dict(zip(recommended_track, recommended_artists))

    track = {
        "name" : df['name'],
        "artist" : artists,
        "duration" : readable_time(df['duration_ms']),
        "album" : df['album']['name'],
        "release" : df['album']['release_date'],
        "img" : df['album']['images'][0]['url'],
        "tracks" : list
    }
    return track

def readable_time(duration):
    minutes = (duration / (60*1000)) % 60
    minutes = int(minutes)
    sec = (duration / 1000) % 60
    sec = int(sec)
    return f"{minutes} minutes and {sec} seconds"