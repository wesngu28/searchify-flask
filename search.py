import pandas as pd
from youtubesearchpython import VideosSearch
from dotenv import load_dotenv
import os

def getAPIKeys():
    load_dotenv()
    env_cid = os.getenv("CID")
    env_sid = os.getenv("SID")
    ids = [];
    if env_cid:
      ids.append(env_cid)
    if env_sid:
      ids.append(env_sid)
    print(ids)
    return ids

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