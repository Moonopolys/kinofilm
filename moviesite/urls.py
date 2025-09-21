from django.urls import path
from .views import (HomeView, AboutView, AddMovieView,
                    delete_movie, update_movie, MoviesByGenreView, profile, MovieDetailView)

urlpatterns = [
    path('', HomeView.as_view(), name='main'),
    path('about/', AboutView.as_view(), name='about'),
    path('movie/add/', AddMovieView.as_view(), name='add_movie'),
    path('movie/<int:movie_id>/delete/', delete_movie, name='delete_movie'),
    path('movie/<int:movie_id>/update/', update_movie, name='update_movie'),
    path('genre/<int:genre_id>/', MoviesByGenreView.as_view(), name='by_genre'),
    path('profile/<str:username>', profile, name='profile'),
    path("movie/<int:movie_id>/", MovieDetailView.as_view(), name='movie_detail'),
]
