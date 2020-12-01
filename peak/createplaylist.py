# -*- coding: UTF-8 -*-
import pickle
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

from dotenv import load_dotenv
import os

#Module to make API requests to spotify more easily
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Import classes from other files
from spotifyclient import *
from track import Track


#Authentication with Spotify API
load_dotenv()
authorization_token = generating_access_token()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
#user_id = get_user_profile()
user_id = os.environ.get('user_id')
#Authentication with Spotipy package
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="https://peak-music.herokuapp.com/", #replace with our website url
                                               scope="playlist-modify-public"))


#Dataframe final
df_kaggle = pd.read_csv('../raw_data/full_dataset.csv')
df_kaggle['year'] = df_kaggle['year'].astype(str) #must be int if used for model


#Display user input as a list of choices
def get_choice(df, column):

    #Gets user choice
    nums = [val for val in range(len(df[column].unique()))]
    choices = list(zip(nums, df[column].unique()))
    print("Select '%s'\n" % column)
    for v in choices:
        print("%s.  %s" % (v))
    user_input = input("Answer: ")
    user_answer = [val[1] for val in choices if val[0]==int(user_input)][0]
    print("'%s' = %s\n" % (column, user_answer))
    return user_answer

def create_spotify_uri(track_id):
        return f"spotify:track:{track_id}"


def main():
    spotify_client = SpotifyClient(authorization_token,user_id)

    #Asking users for their preferences
    query_genre=input("Which genre?\n>")
    query_pop = get_choice(df=df_kaggle, column="popularity_binned")
    query_decade = get_choice(df=df_kaggle, column="decades")
    query_duration = input("Duration of the playlist?\n> ")
    print(f" You selected {query_pop} {query_genre} tracks from the {query_decade} decade for a total duration of {query_duration} minutes")

    #Converting to the right type
    query_pop = str(query_pop)
    query_duration = int(query_duration)
    query_decade = str(query_decade)
    query_genre = str(query_genre)

    #Filtering the dataset accordingly
    filtered_results = df_kaggle[df_kaggle['genres'].str.contains(query_genre) & (df_kaggle['year'].str.contains(query_decade[1:3]))]

    #Get features of 1 random seed track from the filtered_results'
    seed = filtered_results.sample(1)
    tempo = seed['scaled_tempo'].iat[0]
    loudness = seed['scaled_loudness'].iat[0]
    da = seed['danceability'].iat[0]
    energy = seed['energy'].iat[0]

    # couldn't get proper results with loading pickle file , please check
    features_names = ['scaled_tempo', 'scaled_loudness', 'danceability', 'energy'] # 'scaled_year', 'popularity_binned'
    X = filtered_results[features_names]
    y = filtered_results['track_id']
    model = KNeighborsRegressor(algorithm='kd_tree', n_jobs=-1).fit(X, y)


    # get trained model output for k: distances & indices
    knn_out, k = [], 100
    knn_out = model.kneighbors([[tempo,loudness,da,energy]], n_neighbors=k)
    ind = knn_out[1][0].tolist() # get indices
    recs = filtered_results.iloc[ind] # recommendations df

    #filter again upon user input !
    refiltered_results = recs[recs['popularity_binned'] == query_pop]

    #Filter recommendations based on user's preferred duration
    filtered_duration = refiltered_results[refiltered_results['duration_min'].cumsum() <= query_duration]
    recommended_playlist = filtered_duration.reset_index(drop=True)

    #sorting the playlist by tempo
    recommended_playlist.sort_values(by=['scaled_tempo'])
    split_threshold = round(len(recommended_playlist)/2)
    asc_playlist = recommended_playlist.iloc[0:split_threshold].sort_values(by=['scaled_tempo'], ascending=True)
    desc_playlist = recommended_playlist.iloc[split_threshold:].sort_values(by=['scaled_tempo'], ascending=False)
    frames = [asc_playlist, desc_playlist]
    sorted_playlist = pd.concat(frames)
    sorted_playlist = sorted_playlist.reset_index(drop=True)


    recommended_tracks = sorted_playlist[['track_name','track_id','artists']]


    # get playlist name from user and create empty playlist
    playlist_name = input("\nWhat's the playlist name? ")
    playlist_name = str(playlist_name)
    playlist = spotify_client.create_playlist(playlist_name)
    playlist_id =playlist.playlist_id


    # populate playlist with recommended tracks
    tracks_id = sorted_playlist['track_id'].tolist()
    #sp.playlist_add_items(playlist_id, tracks_id, position=None)
    track_uris = [create_spotify_uri(track) for track in tracks_id]
    response = requests.post(
        url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        data = json.dumps(track_uris),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {authorization_token}"
        }
    )
    response = response.json()
    print('Your playlist was successfully added to your spotify account')

if __name__ == "__main__":
    main()
