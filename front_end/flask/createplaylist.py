# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
#Importing stuffs for authentication with Spotify API
from dotenv import load_dotenv
import os
load_dotenv()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
user_id = os.environ.get('user_id')
authorization_token = os.environ.get('authorization_token')

import spotipy
#Authentication with Spotipy package
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= client_id,
                                               client_secret=client_secret,
                                               redirect_uri="https://example.com", #replace with our website url
                                               scope="playlist-modify-public"))

#Import classes from other files
from spotifyclient import SpotifyClient
from track import Track


'''updates michiel'''
from IPython.display import HTML
#Dataframe final

def get_data():
    df_kaggle = pd.read_csv('full_dataset.csv')
    df_kaggle['year'] = df_kaggle['year'].astype(str)
    return df_kaggle

#filter data
def filter_data(genre, decade, popularity, length):
    df_kaggle = get_data()
    filtered_results = df_kaggle[(df_kaggle['genres'].str.contains(str.lower(genre))) & (df_kaggle['decades'] == decade) & (df_kaggle['popularity_binned'] == popularity)]
    if sum(filtered_results['duration_min'].cumsum()) < float(length):
        return False
    return filtered_results

def get_seed(genre, decade, popularity, length):
    filtered_results = filter_data(genre, decade, popularity, length)
    seed = filtered_results.sample(1)
    tempo = seed['scaled_tempo'].iat[0]
    loudness = seed['scaled_loudness'].iat[0]
    da = seed['danceability'].iat[0]
    energy = seed['energy'].iat[0]
    return seed, tempo, loudness, da, energy

def fit_model(genre, decade, popularity, length):
    filtered_results = filter_data(genre, decade, popularity, length)
    features_names = ['scaled_tempo', 'scaled_loudness', 'danceability', 'energy'] # 'scaled_year', 'popularity_binned'
    X = filtered_results[features_names]
    y = filtered_results['track_id']
    model = KNeighborsRegressor(algorithm='kd_tree', n_jobs=-1).fit(X, y)
    return model

def train_model(genre, decade, popularity, length):
    # get trained model output for k: distances & indices
    model = fit_model(genre,decade,popularity, length)
    seed, tempo, loudness, da, energy = get_seed(genre,decade,popularity, length)
    filtered_results = filter_data(genre, decade, popularity, length)
    knn_out, k = [], (len(filtered_results) if len(filtered_results)<100 else 100)
    knn_out = model.kneighbors([[tempo,loudness,da,energy]], n_neighbors=k)
    ind = knn_out[1][0].tolist() # get indices
    recs = filtered_results.iloc[ind] # recommendations df
    return recs

def filter_sort(genre, decade, popularity, length):
    filtered_results2 = train_model(genre, decade, popularity, length)
    filtered_duration = filtered_results2[filtered_results2['duration_min'].cumsum() <= int(length)]
    recommended_playlist = filtered_duration.reset_index(drop=True)
    recommended_tracks = recommended_playlist[['track_name','track_id','artists']]
    return recommended_tracks

def get_name(playlist_name):
    return playlist_name




#Will be replaced by preprocessing pipeline
'''def formatting(df):
    df['genres'] = df['genres'].astype(str)
    df['duration_min'] = (df['duration_ms']/60000).astype(int)
    df['decades'] = pd.cut(x=df['year'], bins=[1920, 1930, 1940, 1950,1960,1970,1980,1990,2000,2010,2020])
    df['year'] = df['year'].astype(str)
    return df'''

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

#def getparam(genre, decade, length, popularity):
    #playlist = [genre, decade, length, popularity]
    #return playlist

# get filtered data for html

def main():
    spotify_client = SpotifyClient(authorization_token,user_id)

    #Asking users for their preferences
    query_genre=input("Which genre?\n>")
    query_pop = input("Popularity? 0 and 100, with 100 being the most popular\n> ")
    query_decade = get_choice(df=get_data(), column="decades")
    query_duration = input("Duration of the playlist?\n> ")
    print(f" You selected {query_genre} tracks with a popularity of {query_pop}% from the {query_decade} decade for a total duration of {query_duration} minutes")

    #Converting to the right type
    query_pop = int(query_pop)
    query_duration = int(query_duration)
    query_decade = str(query_decade)
    query_genre = str(query_genre)

    #filtering the dataset accordingly
    df_kaggle = get_data()
    filtered_genre = df_kaggle[df_kaggle['genres'].str.contains(query_genre)]
    filtered_results = filtered_genre[(filtered_genre['year'].str.contains(query_decade[1:3])) & (filtered_genre['popularity'] == query_pop)]

    # Select 1 random track seed from the filtered_results
    # Insert here the recommendation algorythm from Luam

    # (filtered_results will be replaced by the name of Luam's output dataframe)
    filtered_duration = filtered_results[filtered_results['duration_min'].cumsum() <= query_duration]
    recommended_playlist = filtered_duration.reset_index(drop=True)
    recommended_tracks = recommended_playlist[['track_name','track_id','artists']]
    print(recommended_tracks)


    # get playlist name from user and create playlist
    playlist_name = input("\nWhat's the playlist name? ")
    playlist_name = str(playlist_name)
    playlist = spotify_client.create_playlist(playlist_name)
    playlist_id =playlist.id
    print(f"\nPlaylist '{playlist.name}' was created successfully.")

    # populate playlist with recommended tracks
    tracks_id = recommended_playlist['track_id'].tolist()
    sp.playlist_add_items(playlist_id, tracks_id, position=None)
    print(f"\nRecommended tracks successfully uploaded to playlist '{playlist_name}'.")

if __name__ == "__main__":
    main()
