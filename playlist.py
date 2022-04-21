import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import importlib
import os
import pandas as pd

def playlist_info(sp, URL):
    playlist_tracks_df= sp.playlist_tracks(URL)
    cover_url = sp.playlist_cover_image(URL)
    cover_url = cover_url[0]['url']
    playlist_name = sp.playlist(URL, fields="name")
    playlist_name = playlist_name['name']
    playlist_creation = playlist_tracks_df['items'][0]['added_at']
    playlist_creation = playlist_creation[0:10]
    playlist_size = playlist_tracks_df['total']
    tracks = playlist_tracks_df['items']
    while playlist_tracks_df['next']:
        playlist_tracks_df = sp.next(playlist_tracks_df)
        tracks.extend(playlist_tracks_df['items'])

    playlist_tracks_titles = []
    for track in tracks:
        if(track['track']['id']!=None):
            playlist_tracks_titles.append(track['track']['name'])

    mode_tracker = []
    playlist_tracks_artist = []
    for artist in tracks:
        mode_tracker.append(artist['track']['artists'][0]['name'])
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
    mode  = max(set(mode_tracker), key = mode_tracker.count)
    max_item = mode_tracker.count(mode)
    if(max_item == 1):
        max_item = 'once'
    else:
        max_item = f"{max_item} times"
    list = dict(zip(playlist_tracks_titles, playlist_tracks_artist))
    playlist = {
        "name": playlist_name,
        "size": playlist_size,
        "created": playlist_creation,
        "frequent": mode,
        "frequent_count": max_item,
        "img": cover_url,
        'tracks' : list
    }
    return playlist