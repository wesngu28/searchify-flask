import pandas as pd
from youtubesearchpython import VideosSearch
import random

# Uses the Youtube-Search-Python module to query youtube for corresponding links without a rate limit, appending them to a link list before creating a dataframe.
# I chose to use Pandas due to the ease of making a dataframe instead of having to handle an additional value or run an additional loop in later code to assign the correct link.
# I considered turning this into a flask route or using javascript to handle this to incorporate a progress bar or fetch, but decided against it.
def search_youtube(song_dict):
    link_list = []
    for track in song_dict:
        query = "{} - {}".format(track, song_dict[track])
        videosSearch = VideosSearch(query, limit = 1)
        result = videosSearch.result()
        link = result["result"][0]["link"]
        link_list.append(link)
    df = pd.DataFrame(list(song_dict.items()),columns = ['Song Name','Artists'])
    df['Song Link'] = link_list
    return df

# Function with various random adjectives that are synonyms of awesome found on dictionary.com and various slang
def randomize_adjective():
    adjectives = ['admirable', 'amazing', 'astonishing', 'awesome', 'brilliant', 'cool', 'enjoyable', 'excellent', 'fabulous', 'fantastic', 'fine', 'incredible', 'magnificent', 'marvelous', 'outstanding', 'phenomenal', 'pleasant', 'pleasing', 'remarkable',
    'sensational', 'superb', 'great', 'terrific', 'tremendous', 'wondrous', 'astounding', 'awe-inspiring', 'divine', 'dynamite', 'groovy', 'exquisite', 'miraculous', 'peachy', 'prime', 'staggering', 'stupendous', 'super', 'swell', 'perfect', 'exceptional',
    'perfect', 'smash-hit', 'dynamite', 'breaktaking', 'stunning', 'unbelievable', 'spectacular', 'sublime', 'formidable', 'imposing', 'mind-boggling', 'mind-blowing', 'bussin', 'out of this world', 'amazeballs', 'eye-opening', 'prodigious', 'wonderful',
    'impressive', 'genius', 'mensa-level', 'unique', 'notable', 'life-changing', 'alluring', 'bewitching', 'captivating', 'charming', 'attractive', 'enchanting', 'entertaining', 'banger', 'enthralling', 'fascinating', 'interesting', 'dope', 'fantabulous',
    'grand', 'heavenly', 'high-class', 'hype', 'stellar', 'superior', 'good', 'satisfactory', 'talented', 'legendary', 'worthy of celebrating', 'worthy of worship', 'godlike', 'god-tier', 's-tier', 'immersive', 'bop', 'pog', 'poggingly']
    return random.choice(adjectives)

# Function to convert the duration_ms returned by Spotify to something readable by normal human beings.
def readable_time(duration):
    minutes = (duration / (60*1000)) % 60
    minutes = int(minutes)
    sec = (duration / 1000) % 60
    sec = int(sec)
    return f"{minutes} minutes and {sec} seconds"