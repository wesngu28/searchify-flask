import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import pandas as pd

def artist_info(sp, url):
    df = sp.artist(url)
    genres = df['genres']
    if (len(genres) > 1):
        genres.insert(len(genres)-1, 'and')
        genre_string = ''
        for genre in genres:
            genre_string = genre_string + genre + ', '
        print(genre_string)
        genre_string = genre_string[:-2]
        genre_string = genre_string.replace('and,', 'and')

    name = df['name']
    images = df['images'][0]['url']
    artist = {
        "name" : name,
        "genres" : genres,
        "genre_list" : genre_string,
        "img" : images
    }
    return artist

def artist_recommendations(sp, url):
    url = [url]
    df = sp.recommendations(seed_artists=url, limit=2)
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