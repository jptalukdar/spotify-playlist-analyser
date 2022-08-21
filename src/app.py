import imp
from libs import utilis
from flask import Flask, render_template, request
import analyse_custom_playlist as acp
import find_songs as fs
app = Flask(__name__)

@app.route("/analysis/<name>",methods=['GET', 'POST'])
def analysis(name=None):
  if name is None:
    return "Name is none"
  if name == "url":
    data = request.form.get("url")
    name = data
    print(request.form)
    if data is None:
      args = request.args
      name = str(args.get("url"))
      if name is None:
        return "Data is none"
 
  entity_type, entity_id = utilis.validate_extract_spotify_url(name)
  if entity_type == "playlist":
    results = acp.get_recommendations(entity_id)
    return render_template("playlist.html",track_details=results["tracks"])
  elif entity_type == "track":
    results = fs.get_recommendations(entity_id,limit=10)
    return render_template("playlist.html",track_details=results["tracks"])
  else:
    return f"Unable to extract playlist or track id from url"

@app.route("/",methods=['GET', 'POST'])
def search_page():
  return render_template("index.html")

@app.route("/search",methods=['GET', 'POST'])
def search():
  # data = request.form.get("search")
  # if data is None:
  #   args = request.args
  #   data = str(args.get("search"))
  # results = fs.search_songs(data)
  seeds = fs.get_available_genre()
  print(seeds)
  return render_template("search.html",slider_features=fs.get_feature_set(),available_genre=seeds['genres'])

app.run(host="0.0.0.0" ,port=8000,debug=True)


# https://open.spotify.com/track/spotify:track:4fouWK6XVHhzl78KzQ1UjL?si=247685a0da2a439f