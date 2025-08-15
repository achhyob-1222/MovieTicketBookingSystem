from django.urls import path
from .views import MovieShowtimesView, ShowtimeSeatsView, BookingCreateView

urlpatterns = [
    path('movies/<int:movie_pk>/showtimes/', MovieShowtimesView.as_view(), name='movie-showtimes'),
    path('showtimes/<int:showtime_pk>/seats/', ShowtimeSeatsView.as_view(), name='showtime-seats'),
    path('create/', BookingCreateView.as_view(), name='booking-create'),
]