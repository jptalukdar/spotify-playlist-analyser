import base64
import json
import copy
from . import spotify_connect
import re
def load_playlist(playlist_id):
  with open(f"playlist/{playlist_id}.json","r") as fp:
    playlist = json.load(fp)
  return playlist

def get_tracks_from_playlist(playlist):
  track_id_list = []
  for track in playlist["tracks"]["items"]:
    print(track)
    print(track["track"])
    track_id = track["track"]["id"]
    track_id_list.append(track_id)
  return track_id_list

def get_blank_feature(default):
  return {
    'danceability': copy.deepcopy(default), 
  'energy': copy.deepcopy(default), 
  'key': copy.deepcopy(default), 
  'loudness': copy.deepcopy(default), 
  'mode': copy.deepcopy(default), 
  'speechiness': copy.deepcopy(default), 
  'acousticness': copy.deepcopy(default), 
  'instrumentalness': copy.deepcopy(default), 
  'liveness': copy.deepcopy(default), 
  'valence': copy.deepcopy(default), 
  'tempo': copy.deepcopy(default), 
  }



def get_songs_name_from_mongofinds(finds, track_details):
  song_list = [ track_details.get(x['_id'], spotify_connect.get_track , args=(x['_id'],)) for x in finds ]
  song_names = []
  for index,song in enumerate(song_list):
    try:
      song_names.append(f'{song["track_name"]} by {song["artist_name"]}')
    except KeyError:
      print(json.dumps([song,song_list[index]]))
      
  # song_names = [ f'{x.get("track_name")} by {x.get("artist_name")}' for x in song_list ]
  print(song_names)
  return song_list,song_names


def hash_list(list_of_elements):
  return base64_encode(json.dumps(list_of_elements))

def base64_encode(sample_string):
  sample_string_bytes = sample_string.encode("ascii")
  base64_bytes = base64.b64encode(sample_string_bytes)
  base64_string = base64_bytes.decode("ascii")
  return base64_string


def validate_extract_spotify_url(url:str):
  # https://open.spotify.com/playlist/4G1v4UDYYXCV9dfmvvEkwk?si=9df093ee7cc14419
  if "open.spotify.com" in url:
    url = url.replace("https://open.spotify.com/","")
    if url.startswith("playlist/"):
      return "playlist", url.replace("playlist/","").split("?")[0]
    elif url.startswith("track/"):
      return "track", url.replace("track/","").split("?")[0]
    else:
      return None, None
  elif "spotify:" in url:
    x = re.search("spotify:(track|playlist):([a-zA-Z0-9]*)", url)
    if x is not None:
      r = tuple(x.groups())
      if len(r) != 2:
        print("Unable to extract playlist or track id from url: ", url)
        return None, None
      return r
    else:
      return None, None
  
  return None, None
