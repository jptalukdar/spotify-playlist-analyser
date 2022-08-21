
from libs.data_context_manager import DataBars


instrumental_threshold = 0.5
dance_threshold = 0.5
accoustic_threshold = 0.7
liveness_threshold = 0.8
loudness_threshold = -5
tempo_threshold = 120
valence_threshold = 0.5

def isInstrumental(value: float) -> bool:
  if value > instrumental_threshold:
    return True
  else:
    return False

def isDanceable(value: float) -> bool:
  if value > dance_threshold:
    return True
  else:
    return False

def isAcoustic(value: float) -> bool:
  if value > accoustic_threshold:
    return True
  else:
    return False

def isSad(value: float) -> bool:
  if value > valence_threshold:
    return True
  else:
    return False

def isLoud(value: float) -> bool:
  if value > loudness_threshold:
    return True
  else:
    return False

def isLive(value: float) -> bool:
  if value > liveness_threshold:
    return True
  else:
    return False

# def check_danceability(value: float) -> bool:
#   if value > dance_threshold < : 
#     return True

dance = DataBars("dance")
popularity = DataBars("popularity")
def dance_bars():
  dance.add_bar("Cannot Dance", (0.0, 0.3))
  dance.add_bar("Somewhat Danceable", (0.3, 0.6))
  dance.add_bar("Danceable", (0.6, 0.8))
  dance.add_bar("Very Danceable", (0.8, 1.0))

def popularity_bars():
  popularity.add_bar("Not Many knows about this", (0.0, 10))
  popularity.add_bar("Some know about this", (10, 30))
  popularity.add_bar("Mildly popular", (30, 60))
  popularity.add_bar("Popular", (60, 80))
  popularity.add_bar("Very Popular", (80, 101))

