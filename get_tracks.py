import json
from http.client import HTTPConnection
import sys, urllib.parse
import requests


def main():


    api_endpoint = "http://ws.audioscrobbler.com/2.0/"

    resp = requests.post(url = api_endpoint+ "/2.0/?method=user.getrecenttracks&user=rj&api_key=YOUR_API_KEY&format=json", data = question)
    print(resp.text)



if __name__ == "__main__":
    main()
