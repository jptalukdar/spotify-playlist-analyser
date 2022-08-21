import math
import random
from unittest import result 
from libs import spotify_connect
from libs import utilis
from libs.data_context_manager import DataBlock

rec = DataBlock("recommendations")
tracks = DataBlock("tracks")
audio_features = DataBlock("audio_features")
recommended_tracks = DataBlock("recommended_tracks_from_tracks")

def create_feature(track_id):
  print(audio_features.get(track_id))
  track = audio_features.get(track_id)[0]
  features = {
    "popularity": tracks.get(track_id)["popularity"],
    "danceability": track["danceability"],
    "energy": track["energy"],
    "speechiness": track["speechiness"],
    "acousticness": track["acousticness"],
    "instrumentalness": track["instrumentalness"],
    "liveness": track["liveness"],
    "valence": track["valence"],
    "tempo": track["tempo"],
    "time_signature": track["time_signature"],
    "mode" : track["mode"],
    "duration_min": track["duration_ms"]/(1000*60),
  }
  return features

def recommend_playlist(tracks, feature, playlist_id, **kwargs):
  selected_features = [ 
    "popularity",
    "danceability",
    "energy",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "mode"
  ]
  target_args = { f"target_{key}": feature[key] for key in selected_features }
  print(target_args)

  if isinstance(tracks, list):
    seed_tracks = random.sample(tracks, 5)
  else:
    seed_tracks = [ tracks ]
  r_tracks = rec.raw_get(playlist_id, lambda x: spotify_connect.get_recommendations(seed_tracks, **target_args, **kwargs), no_kwargs=True,**kwargs)
  # r_tracks = spotify_connect.get_recommendations(seed_tracks, **target_args)
  print(r_tracks)
  return r_tracks


"https://open.spotify.com/playlist/4G1v4UDYYXCV9dfmvvEkwk?si=9df093ee7cc14419"
"https://open.spotify.com/playlist/3xDFqWAlHixpXfPdju8asf?si=f3ab084f141045d9"
"https://open.spotify.com/playlist/03ADjnlC31J6AW7Rgb0BU5?si=ff0e8cedaf8448f8"
# playlist_id = "2AgwWY1IGb0W0sYRPYNvAp" # Whiskey tour
# # playlist_id = "4G1v4UDYYXCV9dfmvvEkwk" # Love
# # playlist_id = "3xDFqWAlHixpXfPdju8asf" # Goodies
# playlist_id = "03ADjnlC31J6AW7Rgb0BU5"
search_track_id = "2eAvDnpXP5W0cVtiI0PUxV"


def retrieve_track_info(search_track_id):
  feature_set = {}
  # for track_id in tracks_from_playlist:
  tracks.get(search_track_id,spotify_connect.get_track)
  audio_features.get(search_track_id,spotify_connect.get_track_acoustics)
  feature_set[search_track_id] = create_feature(search_track_id)

  playlist_feature = feature_set[search_track_id]
  playlist_feature["mode"] = round(playlist_feature["mode"])
  playlist_feature["tempo"] = round(playlist_feature["tempo"])
  playlist_feature["popularity"] = round(playlist_feature["popularity"])

  if playlist_feature["instrumentalness"] == 0:
    playlist_feature["instrumentalness"] = 0.1
  
  return playlist_feature

def get_recommendations(search_track_id, **kwargs):
  playlist_feature = retrieve_track_info(search_track_id)
  recommendations = recommend_playlist(search_track_id, playlist_feature, search_track_id, **kwargs)

  tracks_details = []
  for tracks in recommendations["tracks"]:
    song_details = f"""{tracks["name"]} by {tracks["artists"][0]["name"]} | URI: {tracks["uri"]}
    """
    details = {
      "song_title": tracks["name"],
      "song_artist": tracks["artists"][0]["name"],
      "uri": tracks["uri"],
      "embed_uri" : tracks["uri"].replace("spotify:track:","https://open.spotify.com/embed/track/"),
      "track_uri" : tracks["uri"].replace("spotify:track:","https://open.spotify.com/track/"),
      "image_uri": tracks["album"]["images"][0]["url"],
    } 

    tracks_details.append(details)
    tracks.get(tracks["id"],spotify_connect.get_track)
    audio_features.get(tracks["id"],spotify_connect.get_track_acoustics)
    print(song_details)
  results = {"tracks" : tracks_details, "id": search_track_id}
  recommended_tracks.set(search_track_id,results)
  return results

def add_feature(name, id, min, max, default, step=1):
  return {
    "name": name,
    "id": id,
    "min": min,
    "max": max,
    "default": default,
    "step" : (max-min)/100,
  }
def get_feature_set(**kwargs):
  feature_set = []
  feature_set.append(add_feature("popularity", "popularity", 0, 100, 70))
  feature_set.append(add_feature("danceability", "danceability", 0, 1, 0.5))
  feature_set.append(add_feature("energy", "energy", 0, 1, 0.5))
  feature_set.append(add_feature("speechiness", "speechiness", 0, 1, 0.5))
  feature_set.append(add_feature("acousticness", "acousticness", 0, 1, 0.5))
  feature_set.append(add_feature("instrumentalness", "instrumentalness", 0, 1, 0.5))
  feature_set.append(add_feature("liveness", "liveness", 0, 1, 0.5))
  feature_set.append(add_feature("valence", "valence", 0, 1, 0.5))
  feature_set.append(add_feature("tempo", "tempo", 70, 200, 120))
  return feature_set 

def get_available_genre():
  return spotify_connect.get_available_genre()

if __name__ == "__main__":
  r = get_recommendations(search_track_id)
  print(r)