def v2_get_related(request, data, kwargs):
    related_songs_min_length = 7
    s_pk = kwargs['pk']
    s = get_object_or_404(Song, pk=s_pk)
    related_songs = [sg.serialize() for sg in s.uploader.songs.exclude(md5_mp3="").exclude(pk=s_pk).filter(private=False).order_by("-score")[0:related_songs_min_length]]
    rs_n = len(related_songs)
    if rs_n < related_songs_min_length:
        related_songs += [song.serialize() for song in get_rand_top100_by_genre(related_songs_min_length - rs_n, [g.pk for g in s.genres.all()])]
    return related_songs
