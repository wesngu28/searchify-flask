import spotipy
import pandas as pd

def playlist_to_dataframe(sp, URL):
    playlist_tracks_df= sp.playlist_tracks(URL)
    return playlist_tracks_df

def playlist_to_dict(sp, URL):

    playlist_tracks_data = sp.playlist_tracks(URL)

    tracks = playlist_tracks_data['items']
    while playlist_tracks_data['next']:
        playlist_tracks_data = sp.next(playlist_tracks_data)
        tracks.extend(playlist_tracks_data['items'])

    playlist_tracks_artist = []
    playlist_tracks_titles = []
    for track in tracks:
        if(track['track']['id']!=None):
            playlist_tracks_titles.append(track['track']['name'])
            playlist_tracks_artist.append(track['track']['artists'][0]['name'])

    list = dict(zip(playlist_tracks_titles, playlist_tracks_artist))
    return list

def get_Info(sp, URL, df, copy):
    cover_url = sp.playlist_cover_image(URL)
    cover_url = cover_url[0]['url']

    playlist_name = sp.playlist(URL, fields="name")
    playlist_name = playlist_name['name']

    playlist_creation = copy['items'][0]['added_at']
    playlist_creation = playlist_creation[0:10]

    playlist_size = copy['total']

    mode = df['Artist'].value_counts().idxmax()
    item_counts = df['Artist'].value_counts()
    max_item = item_counts.max()

    quickInfo = pd.DataFrame()
    quickInfo['img'] = [cover_url]
    quickInfo['name'] = [playlist_name]
    quickInfo['size'] = [playlist_size]
    quickInfo['frequent'] = [mode]
    quickInfo['frequent_count'] = [str(max_item)]
    return quickInfo