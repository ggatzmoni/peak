#Importing necessary libraries
import json
import requests
import pandas as pd
import os
from dotenv import load_dotenv
#Import classes from other files
from playlist import Playlist
#Authentication with Spotify API
load_dotenv()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
user_id = os.environ.get('user_id')
# Function to generate an authorization_token that lasts longer

def generating_access_token():
    response = requests.post(
        url='https://accounts.spotify.com/api/token',
        data={
        'grant_type':'refresh_token',
        'refresh_token':os.environ.get('refresh_token'),
        'client_id':os.environ.get('CLIENT_ID'),
        'client_secret':os.environ.get('CLIENT_SECRET')
        }
    )
    response = response.json()
    authorization_token = response['access_token']
    return authorization_token

authorization_token = generating_access_token()

class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, authorization_token, user_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self._authorization_token = authorization_token
        self._user_id = user_id


    def create_playlist(self, playlist_name):
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        response = requests.post(
            f"https://api.spotify.com/v1/users/{self._user_id}/playlists",
            json.dumps({
            "name": playlist_name,
            "description": "Recommended songs by Peak",
            "public": True
        }),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {authorization_token}"
            }
        )
        response_json = response.json()
        playlist_id = response_json["id"]

        # create playlist from the class in playlist.py
        playlist = Playlist(playlist_name, playlist_id)
        return playlist

    def create_spotify_uri(track_id):
        return f"spotify:track:{track_id}"
