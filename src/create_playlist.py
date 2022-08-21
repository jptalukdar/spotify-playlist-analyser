from libs import spotify_connect

def create_playlist(tracks, playlist_name, playlist_description, playlist_id=None):
  if playlist_id is None:
    playlist_id = spotify_connect.create_playlist(playlist_name, playlist_description)
  
  spotify_connect.add_to_playlist(playlist_id, tracks)
  return playlist_id