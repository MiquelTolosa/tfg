# Recompute score script
from monkingme import settings
from web_monkingme.models import Song
import datetime


def computeScore(s):
    score = 0
    score += settings.LIKE_FACTOR * s.n_likes
    score += settings.PLAY_FACTOR * s.plays
    score += settings.DOWNLOAD_FACTOR * s.downloads
    now = datetime.datetime.now()
    pub_date = s.pub_date
    days_ago = (now - pub_date.replace(tzinfo=None)).days
    score += settings.DAY_FACTOR * days_ago
    return score


songs = Song.public_valid_objects.all()
print("calculating score for" + str(len(songs)) + " songs...")
for s in songs:
    s.score = computeScore(s)
    s.save()

