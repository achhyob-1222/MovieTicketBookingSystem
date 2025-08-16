from rest_framework import generics, permissions
from .models import Seat, Showtime, Booking
from .serializers import SeatSerializer, BookingSerializer, ShowtimeSerializer, MyBookingSerializer
import datetime

class MyBookingListView(generics.ListAPIView):
    serializer_class = MyBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only future bookings for the logged-in user
        return Booking.objects.filter(
            user=self.request.user,
            showtime__date__gte=datetime.date.today()
        ).order_by('showtime__date', 'showtime__time')

class BookingCancelView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # A user can only cancel their own bookings
        return Booking.objects.filter(user=self.request.user)

class MovieShowtimesView(generics.ListAPIView):
    serializer_class = ShowtimeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        movie_pk = self.kwargs['movie_pk']
        # Get the 'date' from the query parameters (e.g., ?date=2025-08-16)
        show_date_str = self.request.query_params.get('date', None)

        queryset = Showtime.objects.filter(movie_id=movie_pk)

        if show_date_str:
            try:
                # Filter the queryset by the specific date provided
                show_date = datetime.datetime.strptime(show_date_str, '%Y-%m-%d').date()
                queryset = queryset.filter(date=show_date)
            except ValueError:
                # If the date format is invalid, return no results
                return Showtime.objects.none()

        return queryset.order_by('time')

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