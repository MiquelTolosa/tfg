from web_monkingme.models.history import HistoricSongPlay
from datetime import timedelta, datetime
import datetime as dt
import pytz


def product_usage_interval(date_from, ndays):
    # STEP 1
    start_date = date_from - timedelta(days=ndays[0])
    group1 = set()
    not_logged = 0
    plays = HistoricSongPlay.objects.all().filter(datetime__gte=start_date, datetime__lte=date_from)
    for p in plays:
        if not p.user:
            not_logged += 1
        elif p.user.date_joined < start_date:
            group1.add(p.user)
    print("Plays per user: " + str(len(plays) / len(group1)))
    print('Group 1 len: ' + str(len(group1)))
    # STEP 2
    for nday in ndays:
        group2 = set()
        start_date = date_from - timedelta(days=nday)
        for u in group1:
            plays_in_n_days = HistoricSongPlay.objects.all().filter(user=u, datetime__gte=start_date, datetime__lte=date_from)
            len_plays = len(plays_in_n_days)
            if len_plays > 2:
                margin = dt.timedelta(days=1)
                first_play_date = plays_in_n_days[0].datetime
                last_play_date = plays_in_n_days[len_plays - 1].datetime
                if (last_play_date - first_play_date) > margin:
                    group2.add(u)
        print('Group 2 on ' + str(nday) + 'days: ' + str(len(group2)))


date_from = datetime(2017, 4, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
product_usage_interval(date_from, [60, 45, 30, 15, 7, 2])
