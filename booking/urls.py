from django.urls import path
from .views import MovieShowtimesView, ShowtimeSeatsView, BookingCreateView, MyBookingListView,BookingCancelView

urlpatterns = [
    path('movies/<int:movie_pk>/showtimes/', MovieShowtimesView.as_view(), name='movie-showtimes'),
    path('showtimes/<int:showtime_pk>/seats/', ShowtimeSeatsView.as_view(), name='showtime-seats'),
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    # NEW URLs for "Your Tickets"
    path('my-tickets/', MyBookingListView.as_view(), name='my-tickets-list'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]