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
    name = df['name']
    track = {
        "name" : df['name'],
        "artist" : artists,
        "duration" : readable_time(df['duration_ms']),
        "album" : df['album']['name'],
        "release" : df['album']['release_date'],
        "img" : df['album']['images'][0]['url']
    }
    return track

def readable_time(duration):
    minutes = (duration / (60*1000)) % 60
    minutes = int(minutes)
    sec = (duration / 1000) % 60
    sec = int(sec)
    return f"{minutes} minutes and {sec} seconds"

def track_recommendations(sp, url):
    url = [url]
    df = sp.recommendations(seed_tracks=url, limit=2)
    df = df['tracks']
    recommended_track = []
    recommended_artists = []
    for track in df:
        recommended_track.append(track['name'])
        if(len(track['artists']) > 1):
            print(track['artists'])
            artist_count = 0
            artist = ''
            while(artist_count < len(track['artists'])):
                artist = artist + track['artists'][artist_count]['name'] + ', '
                artist_count = artist_count + 1
            artist = artist[:-2]
            recommended_artists.append(artist)
        else:
            recommended_artists.append(track['artists'][0]['name'])
    list = dict(zip(recommended_track, recommended_artists))
    return list