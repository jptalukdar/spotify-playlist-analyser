import pymongo
from . import utilis
from .data_context_manager import DataBlock
from . import spotify_connect

tf = DataBlock("audio_features")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["spotify"]


def insert_audio_features_into_mongodb(playlist_id):
  collection = db["audio_features"]
  playlist = utilis.load_playlist(playlist_id)
  track_id_list = utilis.get_tracks_from_playlist(playlist)

  for track_id in track_id_list:
    feature = tf.get(track_id, spotify_connect.get_track_acoustics)[0]
    if "id" in feature:
      feature["_id"] = feature.pop("id")
    else:
      print("###$###    ",feature)
      continue
    print(feature)
    try:
      collection.insert_one(feature)
    except pymongo.errors.DuplicateKeyError:
      continue

def find_songs_with_similar_acoustics(track_id, scope:float = 0.1):
  feature = tf.get(track_id, spotify_connect.get_track_acoustics)[0]
  print(feature)
  collection = db["audio_features"]
  finds = collection.find({ "$and" : [
     {"acousticness": {"$gt": feature["acousticness"] - scope}},
      {"acousticness": {"$lt": feature["acousticness"] + scope}},
  ]}
  )

  for feature in finds:
    print(feature)

def add_filter(track_id, filter_name:str, filter_value:float):
  feature = tf.get(track_id, spotify_connect.get_track_acoustics)[0]
  # print(feature)
  return [
     {filter_name: {"$gt": feature[filter_name] - filter_value}},
      {filter_name: {"$lt": feature[filter_name] + filter_value}},
  ]

def add_range_filter(feature_name:str, min_value:float, max_value:float):
  return [
     {feature_name: {"$gt": min_value}},
      {feature_name: {"$lt": max_value}},
  ]
def add_static_filter(track_id, filter_name:str):
  feature = tf.get(track_id, spotify_connect.get_track_acoustics)[0]
  # print(feature)
  return [
     {filter_name: feature[filter_name]},
  ]

def add_static_filter_with_value(filter_name:str, filter_value:float):
  return [
     {filter_name: filter_value},
  ]
def find_songs_with_filters(*args):
  collection = db["audio_features"]
  filters = []
  [ filters.extend(x) for x in args]
  fill = { "$and" : filters}

  print(fill)
  finds = collection.find(fill)

  print("Found following songs")

  # for feature in finds:
  #   print(feature)

  return [ x for x in finds]
