from django.urls import path
from .views import MovieDetailView, NowShowingMovieListView, ComingSoonMovieListView

urlpatterns = [
    path('now-showing/', NowShowingMovieListView.as_view(), name='now-showing-movie-list'),
    path('coming-soon/', ComingSoonMovieListView.as_view(), name = 'coming-soon-movie-list'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
]