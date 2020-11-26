'''imports'''
from flask import Flask, redirect, url_for, render_template, request
from function import genre, decade, track, length, popularity

'''instance flask web application'''
app = Flask(__name__)

'''define pages on app'''
# access to page via function decorater - start page
@app.route("/")
# home-app with inline html
def home():
    return render_template("index.html")

# acces to page via parameter
@app.route("/<name>")
#speficy different pages via f string
def user(name):
    return render_template("v1")

#redirect to home when on admin page
@app.route("/admin")
def admin():
    return redirect(url_for("home"))

#create player page
@app.route("/player")
def player():
    return render_template("page_player.html")

@app.route("/v1")
def v1():
    return render_template("v1.html")

@app.route("/v2", methods=["POST","GET"])
def v2():
    genres = genre()
    decades = decade()
    tracks = track()
    lengths = length()
    popularities = popularity()
    return render_template("v2.html", genres=genres, decades=decades, tracks = tracks, lengths = lengths, popularities = popularities)

@app.route("/v3", methods=["POST","GET"])
def v3():
    genres = genre()
    decades = decade()
    tracks = track()
    lengths = length()
    popularities = popularity()
    return render_template("v3.html", genres=genres, decades=decades, tracks = tracks, lengths = lengths, popularities = popularities)

@app.route("/v4", methods=["POST","GET"])
def v4():
    genres = genre()
    decades = decade()
    tracks = track()
    lengths = length()
    popularities = popularity()
    return render_template("v4.html", genres=genres, decades=decades, tracks = tracks, lengths = lengths, popularities = popularities)


@app.route("/center", methods=["POST","GET"])
def center():
    genres = genre()
    decades = decade()
    tracks = track()
    lengths = length()
    popularities = popularity()
    return render_template("center.html", genres=genres, decades=decades, tracks = tracks, lengths = lengths, popularities = popularities)

@app.route("/algo_input", methods=["POST","GET"])
def inp():
    if request.method == "POST":

        req = request.form
        print(req)

        return render_template("algo_running.html")

    return render_template("v3.html")


'''run app'''
if __name__ == "__main__":
    app.run(debug=True)
