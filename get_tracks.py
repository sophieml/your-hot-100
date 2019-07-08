from datetime import datetime
import json
from http.client import HTTPConnection
import pandas as pd
import sys, urllib.parse
import requests
import time


def main():

    with open('sample.json') as f:
        params = json.load(f)
    print(params)
    api_endpoint = "http://ws.audioscrobbler.com/2.0/?"

    tracks = []
    resp = requests.get(url = api_endpoint, params = params)
    page = resp.json()
    n_pages = page['recenttracks']['@attr']['totalPages']
    curr_tracks = page['recenttracks']['track']

    if '@attr' in curr_tracks[0]:
        t = int(time.time())
        tracks.append({'date': datetime.utcfromtimestamp(t).strftime('%d %b %Y, %H:%M'),
                       'date_uts': t,
                       'artist': curr_tracks[0]['artist']['#text'],
                       'album': curr_tracks[0]['album']['#text'],
                       'track': curr_tracks[0]['name'],
                       'album_art_url': curr_tracks[0]['image'][3]['#text']})
        currently_playing = True
        curr_tracks = curr_tracks[1:]
    else:
        currently_playing = False

    for scrobble in curr_tracks:
        tracks.append({'date': scrobble['date']['#text'],
                       'date_uts': scrobble['date']['uts'],
                       'artist': scrobble['artist']['#text'],
                       'album': scrobble['album']['#text'],
                       'track': scrobble['name'],
                       'album_art_url': scrobble['image'][3]['#text']})

    for n in range(2, int(n_pages)+1):
        params['page'] = n
        resp = requests.get(url = api_endpoint, params = params)
        page = resp.json()
        curr_tracks = page['recenttracks']['track']
        if currently_playing:
            curr_tracks = curr_tracks[1:]
        for scrobble in curr_tracks:
            tracks.append({'date': scrobble['date']['#text'],
                           'date_uts': scrobble['date']['uts'],
                           'artist': scrobble['artist']['#text'],
                           'album': scrobble['album']['#text'],
                           'track': scrobble['name'],
                           'album_art_url': scrobble['image'][3]['#text']})
        print("done with page", n)
        time.sleep(0.5)
    tracks = pd.DataFrame(tracks)
    print(tracks)

    tracks.to_csv('data.csv', index = False, encoding = 'utf-8')



if __name__ == "__main__":
    main()
