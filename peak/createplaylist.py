# -*- coding: UTF-8 -*-

from spotifyclient import SpotifyClient
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

import os
import pandas as pd

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
authorization_token = os.environ.get('authorization_token')
user_id = os.environ.get('user_id')
df_kaggle = pd.read_csv('../raw_data/kaggle_df.csv')

def formatting(df):
    df['genres'] = df['genres'].astype(str)
    df['duration_min'] = (df['duration_ms']/60000).astype(int)
    df['decades'] = pd.cut(x=df['year'], bins=[1920, 1930, 1940, 1950,1960,1970,1980,1990,2000,2010,2020])
    df['year'] = df['year'].astype(str)
    return df

def get_choice(data, column):

    #Gets user choice
    nums = [val for val in range(len(data[column].unique()))]
    choices = list(zip(nums, data[column].unique()))
    print("Select '%s'\n" % column)
    for v in choices:
        print("%s.  %s" % (v))
    user_input = input("Answer: ")
    user_answer = [val[1] for val in choices if val[0]==int(user_input)][0]
    print("'%s' = %s\n" % (column, user_answer))
    return user_answer

def main():
    spotify_client = SpotifyClient(authorization_token,user_id)


    #Asking their preferences
    query_genre=input("Which genre?\n>")
    query_pop = input("Popularity? 0 and 100, with 100 being the most popular\n> ")
    query_decade = get_choice(data=formatting(df_kaggle), column="decades")
    query_duration = input("Duration of the playlist?\n> ")
    print(f" You selected {query_genre} tracks with a popularity of {query_pop}% from the {query_decade} decade for a total duration of {query_duration} minutes")

    #Converting to the right type
    query_pop = int(query_pop)
    query_duration = int(query_duration)
    query_decade = str(query_decade)
    query_genre = str(query_genre)

    #filtering the dataset accordingly
    filtered_genre = df_kaggle[df_kaggle['genres'].str.contains(query_genre)]
    filtered_results = filtered_genre[(filtered_genre['year'].str.contains(query_decade[1:3])) & (filtered_genre['popularity'] == query_pop)]

    #Insert here the recommendation algorythm from Luam

    filtered_duration = filtered_results[filtered_results['duration_min'].cumsum() <= query_duration]
    recommended_playlist = filtered_duration.reset_index(drop=True)
    recommended_tracks = recommended_playlist['id'].tolist()
    print(recommended_tracks)

    # get playlist name from user and create playlist
    playlist_name = input("\nWhat's the playlist name? ")
    playlist = spotify_client.create_playlist(playlist_name)
    print(f"\nPlaylist '{playlist.name}' was created successfully.")

    # populate playlist with recommended tracks
    spotify_client.populate_playlist(playlist, recommended_tracks)
    print(f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")


if __name__ == "__main__":
    main()
from spotifyclient import SpotifyClient


def main():
    spotify_client = SpotifyClient(authorization_token,user_id)


    #Asking their preferences
    query_genre=input("Which genre?\n>")
    query_pop = input("Popularity? 0 and 100, with 100 being the most popular\n> ")
    query_decade = get_choice(data=df_kaggle, column="decades")
    query_duration = input("Duration of the playlist?\n> ")
    print(f" You selected {query_genre} tracks with a popularity of {query_pop}% from the {query_decade} decade for a total duration of {query_duration} minutes")

    #Converting to the right type
    query_pop = int(query_pop)
    query_duration = int(query_duration)
    query_decade = str(query_decade)
    query_genre = str(query_genre)

    #filtering the dataset accordingly
    filtered_genre = df_kaggle[df_kaggle['genres'].str.contains(query_genre)]
    filtered_results = filtered_genre[(filtered_genre['year'].str.contains(query_decade[1:3])) & (filtered_genre['popularity'] == query_pop)]
    filtered_duration = filtered_results[filtered_results['duration_min'].cumsum() <= query_duration]
    recommended_playlist = filtered_duration.reset_index(drop=True)
    recommended_tracks = recommended_playlist['id'].tolist()
    print(recommended_tracks)

    # get playlist name from user and create playlist
    playlist_name = input("\nWhat's the playlist name? ")
    playlist = spotify_client.create_playlist(playlist_name)
    print(f"\nPlaylist '{playlist.name}' was created successfully.")

    # populate playlist with recommended tracks
    spotify_client.populate_playlist(playlist, recommended_tracks)
    print(f"\nRecommended tracks successfully uploaded to playlist '{playlist.name}'.")


if __name__ == "__main__":
    main()
