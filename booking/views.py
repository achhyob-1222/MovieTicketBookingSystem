from rest_framework import generics, permissions
from .models import Seat, Showtime
from .serializers import SeatSerializer, BookingSerializer, ShowtimeSerializer

class MovieShowtimesView(generics.ListAPIView):
    serializer_class = ShowtimeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        movie_pk = self.kwargs['movie_pk']
        return Showtime.objects.filter(movie_id=movie_pk).order_by('show_time')

class ShowtimeSeatsView(generics.ListAPIView):
    serializer_class = SeatSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        showtime_pk = self.kwargs['showtime_pk']
        try:
            showtime = Showtime.objects.get(pk=showtime_pk)
            return Seat.objects.filter(hall=showtime.hall).order_by('seat_row', 'seat_number')
        except Showtime.DoesNotExist:
            return Seat.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['showtime_id'] = self.kwargs['showtime_pk']
        return context

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated] # Protect this endpoint