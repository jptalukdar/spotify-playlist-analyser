import spotipy
from catilo import catilo
from spotipy.oauth2 import SpotifyClientCredentials
from .data_context_manager import DataBlock

var = catilo.VariableDirectory()
var.add_file_source("spotify", 4, "/secrets/spotify.json")
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