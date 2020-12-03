'''imports'''
from flask import Flask, redirect, url_for, render_template, request, session
from function import genre, decade, track, length, popularity
from werkzeug.datastructures import ImmutableMultiDict
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


from createplaylist import *
from spotifyclient import *


'''instance flask web application'''
app = Flask(__name__)
app.secret_key = "qsdfghjklm"
#app.config["SECRET_KEY"] = "qsdfghjklm"

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
    widget = session.get('playlist_id_widget')
    print(widget)
    return render_template("page_player.html", widget=widget)

@app.route("/error", methods=["POST","GET"])
def error():
    return render_template("experiment.html")

#@app.route("/algo_running", methods=["POST","GET"])
#def algo_running():
    #return render_template("algo_running.html", length=length, genre=genre, decade=decade, popularity=popularity)

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
        genre, decade, length, popularity, playlist_name = req.values()
        #specify function to input front-end and return html page
        if filter_data(genre, decade, length, popularity) is False:
            return redirect("/error")
        playlist_id = get_playlist_id(playlist_name)
        session['playlist_id_widget'] = playlist_id
        add_items_to_playlist(genre, decade, length, popularity, playlist_name, playlist_id)
        return redirect("/page_player")

    return render_template("error.html")

#@app.route("/playlist_input", methods=["POST","GET"])
#def playlist_input():
    #if request.method == "POST":
        #playlist_req = request.form['playlist_name']
        #playlist_id = get_playlist_id(playlist_req)
        #spoti = add_items_to_playlist(genre, decade, popularity, length, playlist_req, playlist_id)
        #print(spoti)
        #return render_template('page_player.html', playlist_name=playlist_name)
    #return redirect("/error")

'''run app'''
if __name__ == "__main__":
    app.run(debug=True)
