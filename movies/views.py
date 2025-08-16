from rest_framework import generics, permissions
from .models import Movie
from .serializers import MovieSerializer
from django.utils import timezone

class NowShowingMovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Movie.objects.filter(release_date__lte=timezone.now().date()).order_by('-release_date')

class ComingSoonMovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Movie.objects.filter(release_date__gt=timezone.now().date()).order_by('release_date')


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]


