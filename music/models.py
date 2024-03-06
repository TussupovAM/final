from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    artistName = models.CharField(_("Artist Name"), max_length=50)
    created = models.DateTimeField(_("Artist created date"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Latest artist update"), auto_now=True)
    verificated = models.BooleanField(default=False)
    class Meta:
        verbose_name = _("Artist")
        verbose_name_plural = _("Artists")

    def __str__(self):
        return self.artistName

    def total_likes(self):
        return sum(song.liked_by.count() for album in self.album_set.all() for song in album.song_set.all())

    def add_song(self, song):
        # Add a song to the album
        song.album = self
        song.save()


class Album(models.Model):
    artist = models.ForeignKey("Artist", verbose_name=_("Artist Album"), on_delete=models.CASCADE)
    albumName = models.CharField(_("Album Name"), max_length=50)
    created = models.DateTimeField(_("Album created date"), auto_now_add=True)
    last_updated = models.DateTimeField(_("Latest album update"), auto_now=True)

    class Meta:
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")

    def __str__(self):
        return self.albumName


class Song(models.Model):
    album = models.ForeignKey("Album", verbose_name=_("Song Album"), on_delete=models.CASCADE)
    songThumbnail = models.ImageField(_("Song Thumbnail"), upload_to='thumbnail/',
                                      help_text=".jpg, .png, .jpeg, .gif, .svg supported")
    song = models.FileField(_("Song"), upload_to='songs/', help_text=".mp3 supported only", )
    songName = models.CharField(_("Song Name"), max_length=50)
    created = models.DateTimeField(_("Song created date"), auto_now_add=True)
    song_genre = models.CharField(null='True')
    song_mood = models.CharField(null="True")
    last_updated = models.DateTimeField(_("Latest song update"), auto_now=True)
    liked_by = models.ManyToManyField(User, related_name='liked_songs', blank=True)
    class Meta:
        verbose_name = _("Song")
        verbose_name_plural = _("Songs")

    def __str__(self):
        return self.songName

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, related_name='playlists')