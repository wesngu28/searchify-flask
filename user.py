import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

def user_info(sp):
    df = sp.current_user()
    return df