'''imports'''
from flask import Flask, redirect, url_for, render_template, request, session
from function import genre, decade, track, length, popularity
from werkzeug.datastructures import ImmutableMultiDict
from dotenv import load_dotenv
import os
load_dotenv()
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
user_id = os.environ.get('user_id')
authorization_token = os.environ.get('authorization_token')
from createplaylist import filter_data, get_seed, fit_model, train_model, filter_sort

import spotipy
#Authentication with Spotipy package
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= client_id,
                                               client_secret=client_secret,
                                               redirect_uri="https://example.com", #replace with our website url
                                               scope="playlist-modify-public"))

#Import classes from other files
from spotifyclient import *

'''instance flask web application'''
app = Flask(__name__)

#config parameters database



'''create DB'''


'''define pages on app'''
# access to page via function decorater - start page
#@app.route("/")
# home-app with inline html
#def home():
    #return render_template("index.html")

# acces to page via parameter
#@app.route("/<name>")
#speficy different pages via f string
#def user(name):
    #return render_template("v1")

#redirect to home when on admin page

#create player page
#@app.route("/player", methods=['POST','GET'])
#def player():
    #if request.main == 'POST':
        #msg = request.form.get('msg')
        #print(msg)
    #return render_template("player.html", main=main)

#@app.route("/v1")
#def v1():
    #return render_template("v1.html")

@app.route("/algo_running", methods=["POST","GET"])
def algo():
    return render_template("algo_running.html")

@app.route("/playlist", methods=["POST","GET"])
def playlist():
    return render_template("playlist.html")

@app.route("/page_player", methods=["POST","GET"])
def page_player():
    return render_template("page_player.html", length=length, genre=genre, decade=decade, popularity=popularity)

@app.route("/error", methods=["POST","GET"])
def error():
    return render_template("experiment.html")

@app.route("/algo_running", methods=["POST","GET"])
def algo_running():
    return render_template("algo_running.html", length=length, genre=genre, decade=decade, popularity=popularity)

@app.route("/", methods=["POST","GET"])
def center():
    genres = genre()
    decades = decade()
    tracks = track()
    lengths = length()
    popularities = popularity()
    return render_template("center.html", genres=genres, decades=decades, tracks = tracks, lengths = lengths, popularities = popularities)


@app.route("/algo_input", methods=["POST","GET"])
def algo_input():
    if request.method == "POST":
        req = request.form
        genre, decade, length, popularity = req.values()
        #specify function to input front-end and return html page
        if filter_data(genre, decade, popularity, length) is False:
            return redirect("/error")
        result = filter_sort(genre, decade, popularity, length)
        #session['genre'] = 'rock'

        return render_template('algo_running.html', length=length, genre=genre, decade=decade, popularity=popularity)  #redirect('/algo_running'

    return render_template("center.html")

@app.route("/playlist_input", methods=["POST","GET"])
def playlist_input():
    if request.method == "POST":
        playlist_name = request.form['playlist_name']
        return render_template('page_player.html', playlist_name=playlist_name)
    return redirect("/error")

'''run app'''
if __name__ == "__main__":
    app.run(debug=True)
