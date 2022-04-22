import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

def album_info(sp, url):
  df = sp.album(url)
  artists = ''
  for information in df['artists']:
    artists = artists + information['name'] + ', '
  artists = artists[:-2]

  tracks = []
  for track in df['tracks']['items']:
    tracks.append(track['name'])

  artist_list = df['tracks']['items']
  playlist_tracks_artist = []
  assumed_main_artist = ''
  for artist in artist_list:
      if (len(artist['artists']) > 1):
          artist_counter = 0
          artist_list = ''
          while (len(artist['artists']) > artist_counter):
              artist_list = artist_list + artist['artists'][artist_counter]['name'] + ', '
              artist_counter = artist_counter + 1
          artist_list = artist_list[:-2]
          playlist_tracks_artist.append(artist_list)
      else:
          playlist_tracks_artist.append(artist['artists'][0]['name'])
          assumed_main_artist = artist['artists'][0]['name']

  list = dict(zip(tracks, playlist_tracks_artist))
  album = {
    'name' : df['name'],
    'total_tracks' : df['total_tracks'],
    'release_date' : df['release_date'],
    'artists' : artists,
    'img' : df['images'][0]['url'],
    'tracks' : list,
    'main_artist' : assumed_main_artist
  }
  return album