def get_myrecommended(request, data, kwargs):
    """
    Returns songs recommended for a user
    """
    recommendation_size = 7
    plays_needed = 10
    rs = []
    u = request.user
    up = u.user_profile

    # Liked
    liked_songs = up.s_likes.all()
    #liked_artists = up.likes.all()
    liked_genres = up.liked_genres.all()

    # Recommended songs from liked songs
    n_from_liked_songs = 3
    for s in get_random_from_list(n_from_liked_songs, liked_songs):
        provs = _get_nth_element(_get_recommended(s, u), 0)
        if provs not in rs:
            rs.append(provs)

    # Recommended songs from liked artists (top songs)
    rand_linked_arts = get_random_from_list(2, liked_artists)
    s_most_played = a.songs.all().filter(private=False, uploader__id__in=rand_linked_arts).order_by("-score")
    if(len(s_most_played) > 0):
        provs = s_most_played[0].serialize()
        if provs not in rs:
            rs.append(provs)
    
    #Recommend songs from liked genres
    n_from_liked_genres = 3
    if(len(liked_genres)):
        get_rand_top100_by_genre(n_from_liked_genres, liked_genres)
    else:
        get_rand_top100(n_from_liked_genres, plays_needed)

    # Fill with newest songs with more than x plays
    if len(liked_genres):
        q_list = []
        for g in liked_genres:
            q_list.append(Q(genres__id__exact=g.pk))
        newest = Song.public_valid_objects.filter(reduce(operator.or_, q_list)).filter(plays__gte=plays_needed).order_by("-pub_date")[0:(recommendation_size - len(rs))]
        for s in newest:
            rs.append(s)

    # Fill it with random top 100 songs
    if recommendation_size != len(rs):
        newest = get_rand_top100(recommendation_size - len(rs), plays_needed)
        for s in newest:
            rs.append(s)

    return [s.serialize() for s in rs]

