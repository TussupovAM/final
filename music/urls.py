
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import like_song, liked_songs

urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('', views.index, name="index"),
    path('logout', views.logout, name='logout'),
    path('like_song/<int:song_id>/', like_song, name='like_song'),
    path('liked_songs/', liked_songs, name='liked_songs'),
    # path('profile/<str:pk>/', views.profile, name='profile'),
    path('search-songs/', views.search_songs, name='search_songs'),
]  + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)