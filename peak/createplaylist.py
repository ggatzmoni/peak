# -*- coding: UTF-8 -*-
import pandas as pd
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
#Import classes from other files
from spotifyclient import *
from track import Track
from final_knn import get_seed_features, get_k_dist_ind
#Authentication with Spotify API
load_dotenv()
authorization_token = generating_access_token()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
user_id = os.environ.get('user_id')
#Authentication with Spotipy package
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="https://example.com", #replace with our website url
                                               scope="playlist-modify-public"))

#Import classes from other files
from spotifyclient import SpotifyClient
from track import Track

#Dataframe final
df_kaggle = pd.read_csv('../raw_data/full_dataset.csv')
df_kaggle['year'] = df_kaggle['year'].astype(str) #must be int if used for model


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

def main():
    spotify_client = SpotifyClient(authorization_token,user_id)

    #Asking users for their preferences
    query_genre=input("Which genre?\n>")
    query_pop = input("Popularity? 0 and 100, with 100 being the most popular\n> ")
    query_decade = get_choice(df=df_kaggle, column="decades")
    query_duration = input("Duration of the playlist?\n> ")
    print(f" You selected {query_genre} tracks with a popularity of {query_pop}% from the {query_decade} decade for a total duration of {query_duration} minutes")

    #Converting to the right type
    query_pop = int(query_pop)
    query_duration = int(query_duration)
    query_decade = str(query_decade)
    query_genre = str(query_genre)

    #Filtering the dataset accordingly
    filtered_genre = df_kaggle[df_kaggle['genres'].str.contains(query_genre)]
    filtered_results = filtered_genre[(filtered_genre['year'].str.contains(query_decade[1:3])) & (filtered_genre['popularity'] == query_pop)]

    #Get features of 1 random seed track from the filtered_results
    tempo, loudness, da, energy = get_seed_features(filtered_results)
    #Use trained knn model to get k=100 recommendations df
    knn_trained = pickle.load(open("knn_trained.pkl","rb")) # load trained model
    knn_out = get_k_dist_ind(knn_trained, tempo, loudness, da, energy) # get output: distances & indices
    indices = knn_out[1][0].tolist() # get indices
    recs = filtered_results.iloc[ind] # recommendations df

    #Filter recommendations based on user's preferred duration
    filtered_duration = recs[recs['duration_min'].cumsum() <= query_duration]
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
