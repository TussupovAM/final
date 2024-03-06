from django.contrib.postgres.search import SearchQuery
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Song, Album, Artist
from .forms import AlbumForm, SongForm

def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.artist = request.user.artist
            album.save()
            return redirect('profile', artist_id=request.user.artist.id)
    else:
        form = AlbumForm()

    return render(request, 'base/create_album.html', {'form': form})

def album_profile(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    songs = album.song_set.all()

    return render(request, 'base/album_profile.html', {'album': album, 'songs': songs})

def add_song_to_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id, artist=request.user.artist)

    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.album = album
            song.save()
            return redirect('album_profile', album_id=album.id)
    else:
        form = SongForm()

    return render(request, 'base/add_song_to_album.html', {'form': form, 'album': album})
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    allSongs = Song.objects.all().order_by('-last_updated')
    return render(request, template_name="base/index.html", context={"allSongs": allSongs,'song': Song})



# def search_songs(request):
#
#     search_query = request.GET.get('search')
#
#     if search_query:
#         search_result = Song.objects.filter(
#             Q(songName__icontains=search_query) |
#             Q(album__albumName__icontains=search_query) |
#             Q(album__artist__artistName__icontains=search_query)
#         ).distinct()
#     else:
#         search_result = Song.objects.all()
#
#     context = {'search_result': search_result, 'search_query': search_query}
#     return render(request, 'base/search_result.html', context)
def search_songs(request):
    search_query = request.GET.get('search_query', '')
    search_result = (
        Song.objects
        .filter(Q(songName__icontains=search_query) |
                Q(song_genre__icontains=search_query) |
                Q(song_mood__icontains=search_query))
    )
    return render(request, 'base/search_result.html', {'search_result': search_result, 'search_query': search_query})
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'base/login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'base/signup.html')

def like_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)

    if request.user in song.liked_by.all():
        song.liked_by.remove(request.user)
    else:
        song.liked_by.add(request.user)

    return redirect('/')

@login_required
def liked_songs(request):
    # Get the songs liked by the current user
    liked_songs = Song.objects.filter(liked_by=request.user)

    return render(request, 'base/liked_songs.html', {'liked_songs': liked_songs})


def artist_profile(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    albums = Album.objects.filter(artist=artist)
    total_likes = artist.total_likes()

    return render(request, 'base/artist_profile.html', {'artist': artist, 'albums': albums, 'total_likes': total_likes})
