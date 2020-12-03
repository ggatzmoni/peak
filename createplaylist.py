# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
#Importing stuffs for authentication with Spotify API
from dotenv import load_dotenv
import os
load_dotenv()

is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    user_id = os.environ.get('user_id')
    redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')
else:
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    user_id = os.getenv('user_id')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
#Import classes from other files

from spotifyclient import *
authorization_token = generating_access_token()

from playlist import *

'''updates michiel'''
from IPython.display import HTML
#Dataframe final

def get_data():
    df_kaggle = pd.read_csv('full_dataset_new.csv')
    df_kaggle['year'] = df_kaggle['year'].astype(str)
    return df_kaggle

#filter data
def filter_data(genre, decade, length, popularity):
    df_kaggle = get_data()
    filtered_results = df_kaggle[(df_kaggle['genres'].str.contains(str.lower(genre))) & (df_kaggle['decades'] == decade) & (df_kaggle['popularity_binned'] == popularity)]
    if sum(filtered_results['duration_min'].cumsum()) < float(length):
        return False
    return filtered_results

def get_seed(genre, decade, length, popularity):
    filtered_results = filter_data(genre, decade, length, popularity)
    if genre == "Techno":
         seed = filtered_results.sample(1)
    elif genre =="Classical":
        seeds = filtered_results[filtered_results['genres'].str.contains(str.lower(f"'{genre}',"))]
        seed = seeds.sample(1)
    else:
        seeds = filtered_results[filtered_results['genres'].str.contains(str.lower(f", {genre},"))]
        seed = seeds.sample(1)
    tempo = seed['scaled_tempo'].iat[0]
    da = seed['danceability'].iat[0]
    energy = seed['energy'].iat[0]
    return seed, tempo, da, energy

def fit_model(genre, decade, length, popularity):
    filtered_results = filter_data(genre, decade, length, popularity)
    features_names = ['scaled_tempo', 'danceability', 'energy'] # 'scaled_year', 'popularity_binned'
    X = filtered_results[features_names]
    y = filtered_results['track_id']
    model = KNeighborsRegressor(algorithm='kd_tree', n_jobs=-1).fit(X, y)
    return model

def train_model(genre, decade, length, popularity):
    # get trained model output for k: distances & indices
    model = fit_model(genre, decade, length, popularity)
    seed, tempo, da, energy = get_seed(genre, decade, length, popularity)
    filtered_results = filter_data(genre, decade, length, popularity)
    knn_out, k = [], (len(filtered_results)-1 if len(filtered_results)<100 else 100)
    knn_out = model.kneighbors([[tempo,da,energy]], n_neighbors=k)
    ind = knn_out[1][0].tolist() # get indices
    recs = filtered_results.iloc[ind] # recommendations df
    return recs

def filter_sort(genre, decade, length, popularity):
    filtered_results2 = train_model(genre, decade, length, popularity)
    filtered_duration = filtered_results2[filtered_results2['duration_min'].cumsum() <= int(length)]
    recommended_playlist = filtered_duration.reset_index(drop=True)
    recommended_playlist.sort_values(by=['scaled_tempo'])
    split_threshold = round(len(recommended_playlist)/2)
    asc_playlist = recommended_playlist.iloc[0:split_threshold].sort_values(by=['scaled_tempo'], ascending=True)
    desc_playlist = recommended_playlist.iloc[split_threshold:].sort_values(by=['scaled_tempo'], ascending=False)
    frames = [asc_playlist, desc_playlist]
    sorted_playlist = pd.concat(frames)
    sorted_playlist = sorted_playlist.reset_index(drop=True)
    recommended_tracks = sorted_playlist[['track_name','track_id','artists']]
    return recommended_tracks

def get_tracks_id(genre, decade, length, popularity):
    sorted_playlist = filter_sort(genre, decade, length, popularity)
    tracks_id = sorted_playlist['track_id'].tolist()
    return tracks_id

def get_playlist_id(playlist_name):
    playlist_id = create_playlist2(playlist_name)
    #playlist_id = playlist.playlist_id
    return playlist_id

def add_items_to_playlist(genre, decade, length, popularity, playlist_name, playlist_id):
## populate playlist with recommended tracks
    tracks_id = get_tracks_id(genre, decade, length, popularity)
    track_uris = [create_spotify_uri2(track) for track in tracks_id]
    #playlist_id = get_playlist_id(playlist_name)
    response = requests.post(
        url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        data = json.dumps(track_uris),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {authorization_token}"
        }
    )
    response = response.json()
    return response
