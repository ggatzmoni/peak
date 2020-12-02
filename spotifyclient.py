#Importing necessary libraries
import json
import requests
import pandas as pd
#Importing stuffs for authentication with Spotify API
import os
from dotenv import load_dotenv
load_dotenv()

if is_prod:
    import boto3
    from boto.s3.connection import S3Connection
    user_id = S3Connection(os.environ['user_id'])
    client_id = S3Connection(os.environ['CLIENT_ID'])
    client_secret = S3Connection(os.environ['CLIENT_SECRET'])
    redirect = S3Connection(os.environ['SPOTIPY_REDIRECT_URI'])
    refresh_token = S3Connection(os.environ['refresh_token'])
else:
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    user_id = os.environ.get('user_id')
    redirect = os.environ.get('SPOTIPY_REDIRECT_URI')
    refresh_token = os.environ.get('refresh_token')

#Import classes from other files
from playlist import Playlist


##Added this function here
def generating_access_token():
    response = requests.post(
        url='https://accounts.spotify.com/api/token',
        data={
        'grant_type':'refresh_token',
        'refresh_token':refresh_token,
        'client_id':client_id,
        'client_secret':client_secret
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

    def create_spotify_uri(track_id):
        return f"spotify:track:{track_id}"
