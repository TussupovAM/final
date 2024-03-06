# forms.py
from django import forms
from .models import Album, Song

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['albumName']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['songThumbnail', 'song', 'songName', 'song_genre', 'song_mood']
