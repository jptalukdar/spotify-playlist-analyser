import spotipy
from catilo import catilo
from spotipy.oauth2 import SpotifyClientCredentials
from .data_context_manager import DataBlock

var = catilo.VariableDirectory()
def load_file(var:catilo.VariableDirectory, path:str, priority:int=4):
  try:
     var.add_file_source("spotify", priority, path)
  except Exception as e:
    print(e)
    pass
load_file(var,"/secrets/spotify.json" )
load_file(var,"secrets/spotify.json" )
var.enable_environment_vars(prefix="SPOTIFY_")

CLIENT_ID = var.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = var.get("SPOTIFY_CLIENT_SECRET")

playlist = DataBlock("playlist")
sf = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
  client_id=CLIENT_ID,
  client_secret=CLIENT_SECRET,
))

def get_track_acoustics(track_id, **kwargs):
  track = sf.audio_features(track_id)
  return track

def get_track(track_id, **kwargs):
  track = sf.track(track_id)
  return track

def get_recommendations(track_id, **kwargs):
  if isinstance(track_id, list):
    seed_tracks = track_id
  else:
    seed_tracks = [track_id]
  recommendations = sf.recommendations(seed_tracks=seed_tracks, **kwargs)
  return recommendations

def get_playlist(playlist_id, **kwargs):
  play = playlist.get(playlist_id, sf.playlist, no_kwargs=True)
  # play = sf.playlist(playlist_id)
  return play

genre = DataBlock("genre")
def get_available_genre(**kwargs):
  genres = genre.get("genre",sf.recommendation_genre_seeds, no_kwargs=True, no_args=True)
  return genres

def create_playlist(name, **kwargs):
  playlist = sf.user_playlist_create(sf.current_user()["id"], name, public=True, description="")
  return playlist

def add_to_playlist(playlist_id, tracks, **kwargs):
  for track in tracks:
    sf.user_playlist_add_tracks(sf.current_user()["id"], playlist_id, track)
  return True