def get_rand_top100_by_genre(N, genres):
    songs = Song.public_valid_objects.filter(genres__in=genres).order_by('-score')[:100]
    return get_random_from_list(N, songs)


def get_rand_top100(N, plays_needed):
    songs = Song.public_valid_objects.order_by('-score')[:100]
    return get_random_from_list(N, songs)
