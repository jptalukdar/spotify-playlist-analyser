import imp
from libs import utilis, spotify_connect
from flask import Flask, render_template, request
import create_playlist as cp
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
    results, source = acp.get_recommendations(entity_id)
    return render_template("playlist.html",track_details=results["tracks"], source=source)
  elif entity_type == "track":
    results, source = fs.get_recommendations(entity_id,limit=10)
    return render_template("playlist.html",track_details=results["tracks"], source=source)
  else:
    return render_template("404.html")

# @app.route("/create/<name>",methods=['GET', 'POST'])
# def create_playlist(name=None):
#   if name is None:
#     return "Name is none"
#   if name == "url":
#     data = request.form.get("url")
#     name = data
#     print(request.form)
#     if data is None:
#       args = request.args
#       name = str(args.get("url"))
#       if name is None:
#         return "Data is none"
 
#   entity_type, entity_id = utilis.validate_extract_spotify_url(name)
#   if entity_type == "playlist":
#     results, source = acp.get_recommendations(entity_id)
#     # return render_template("playlist.html",track_details=results["tracks"], source=source)
#   elif entity_type == "track":
#     results, source = fs.get_recommendations(entity_id,limit=10)
#     # return render_template("playlist.html",track_details=results["tracks"], source=source)
#   else:
#     return render_template("404.html")
  
#   play = cp.create_playlist(results["tracks"],
#       playlist_name=f'{source["name"]} - {source["author"]} - {source["type"]}' , 
#       playlist_description=f'Awesome playlist based on {source["type"]} : {source["name"]} By {source["author"]}')
#   return render_template("playlist.html",track_details=results["tracks"], source=source, playlist_created=True)


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

if __name__ == "__main__":
  app.run(host="0.0.0.0" ,port=8000,debug=True)


# https://open.spotify.com/track/spotify:track:4fouWK6XVHhzl78KzQ1UjL?si=247685a0da2a439f