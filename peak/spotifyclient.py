#Importing necessary libraries
import json
import requests
import pandas as pd

#Importing stuffs for authentication with Spotify API
import os
from dotenv import load_dotenv
load_dotenv()

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
authorization_token = os.environ.get('authorization_token')
user_id = os.environ.get('user_id')

#Import classes from other files
from track import Track
from playlist import Playlist

#Dataframe final
df_kaggle = pd.read_csv('../raw_data/kaggle_df.csv')

class SpotifyClient:
    """SpotifyClient performs operations using the Spotify API."""

    def __init__(self, authorization_token, user_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (str): Spotify user id
        """
        self._authorization_token = authorization_token
        self._user_id = user_id


    def create_playlist(self, name):
        """
        :param name (str): New playlist name
        :return playlist (Playlist): Newly created playlist
        """
        response = requests.post(
            f"https://api.spotify.com/v1/users/{self._user_id}/playlists",
            json.dumps({
            "name": name,
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
        playlist = Playlist(name, playlist_id)
        return playlist


    '''def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response

    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._authorization_token}"
            }
        )
        return response'''
