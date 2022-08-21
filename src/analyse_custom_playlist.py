import random
from unittest import result 
from libs import spotify_connect
from libs import utilis
from libs.data_context_manager import DataBlock

rec = DataBlock("recommendations")
tracks = DataBlock("tracks")
audio_features = DataBlock("audio_features")
recommended_tracks = DataBlock("recommended_tracks")


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
  seed_tracks = random.sample(tracks, 5)
  playlist_id = f"playlist_{playlist_id}"
  if rec.check_cache(playlist_id):
    return rec.get(playlist_id)
  else:  
    r_tracks = spotify_connect.get_recommendations(seed_tracks, **target_args)
  # r_tracks = rec.get(playlist_id, lambda x: , no_kwargs=True, **kwargs)
  # r_tracks = spotify_connect.get_recommendations(seed_tracks, **target_args)
  print(r_tracks)
  return r_tracks


"https://open.spotify.com/playlist/4G1v4UDYYXCV9dfmvvEkwk?si=9df093ee7cc14419"
"https://open.spotify.com/playlist/3xDFqWAlHixpXfPdju8asf?si=f3ab084f141045d9"
"https://open.spotify.com/playlist/03ADjnlC31J6AW7Rgb0BU5?si=ff0e8cedaf8448f8"
playlist_id = "2AgwWY1IGb0W0sYRPYNvAp" # Whiskey tour
# playlist_id = "4G1v4UDYYXCV9dfmvvEkwk" # Love
# playlist_id = "3xDFqWAlHixpXfPdju8asf" # Goodies
playlist_id = "03ADjnlC31J6AW7Rgb0BU5"

def retrieve_playlist_info(playlist_id):
  playlist = spotify_connect.get_playlist(playlist_id)
  tracks_from_playlist = utilis.get_tracks_from_playlist(playlist)
  feature_set = {}
  for track_id in tracks_from_playlist:
    tracks.get(track_id,spotify_connect.get_track)
    audio_features.get(track_id,spotify_connect.get_track_acoustics)
    feature_set[track_id] = create_feature(track_id)
  return tracks_from_playlist,feature_set,playlist

def create_target_features(feature_set):
  average_feature_set = {}
  for track_id,feature in feature_set.items():
    for f in feature:
      if f not in average_feature_set:
        average_feature_set[f] = feature[f]
      else:
        average_feature_set[f] += feature[f]

  playlist_feature = { f: average_feature_set[f]/len(feature_set) for f in average_feature_set }

  playlist_feature["mode"] = round(playlist_feature["mode"])
  playlist_feature["tempo"] = round(playlist_feature["tempo"])
  playlist_feature["popularity"] = round(playlist_feature["popularity"])
  print("PLAYLIST FEATURE",playlist_feature)
  return playlist_feature


def get_recommendations(playlist_id, **kwargs):
  tracks_from_playlist, feature, playlist = retrieve_playlist_info(playlist_id)
  playlist_feature = create_target_features(feature)
  recommendations = recommend_playlist(tracks_from_playlist, playlist_feature, playlist_id)

  print("RECOMMENDATIONS",recommendations)
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

  source = {
    "type" : "track",
    "id" : f"spotify:playlist:{playlist_id}",
    "name" : playlist['name'],
    "author" : playlist['owner']['display_name'],
  }
  results = {"tracks" : tracks_details, "id": playlist_id, "name": playlist["name"]}
  recommended_tracks.set(playlist_id,results)
  return results, source


if __name__ == "__main__":
  get_recommendations(playlist_id)