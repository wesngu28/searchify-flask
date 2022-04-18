import pandas as pd
from youtubesearchpython import VideosSearch

def search_youtube(song_dict):
    link_list = []
    for track in song_dict:
        query = "{} - {}".format(track, song_dict[track])
        videosSearch = VideosSearch(query, limit = 1)
        result = videosSearch.result()
        link = result["result"][0]["link"]
        link_list.append(link)

    df = pd.DataFrame(list(song_dict.items()),columns = ['Song Name','Artist'])
    df['Song Link'] = link_list
    return df