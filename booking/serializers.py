from rest_framework import serializers
from .models import Seat, Booking, BookedSeat, Showtime, CinemaHall
from movies.models import Movie


# Nested serializers to show detailed information
class MovieTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title',)


class HallNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ('name',)


class ShowtimeDetailSerializer(serializers.ModelSerializer):
    movie = MovieTitleSerializer()
    hall = HallNameSerializer()

    class Meta:
        model = Showtime
        fields = ('id', 'date', 'time', 'movie', 'hall')


class BookedSeatDetailSerializer(serializers.ModelSerializer):
    # Custom field to combine row and number
    seat_label = serializers.SerializerMethodField()

    class Meta:
        model = BookedSeat
        fields = ('seat_label',)

    def get_seat_label(self, obj):
        return f"{obj.seat.seat_row}{obj.seat.seat_number}"


# Main serializer for the "Your Tickets" page
class MyBookingSerializer(serializers.ModelSerializer):
    showtime = ShowtimeDetailSerializer()
    booked_seats = BookedSeatDetailSerializer(many=True)

    class Meta:
        model = Booking
        fields = ('id', 'showtime', 'booked_seats', 'booking_time')


class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = ('id', 'date', 'time')


class SeatSerializer(serializers.ModelSerializer):
    is_booked = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ('id', 'seat_row', 'seat_number', 'is_booked')

    def get_is_booked(self, obj):
        showtime_id = self.context.get("showtime_id")
        if not showtime_id:
            return False
        return BookedSeat.objects.filter(
            seat=obj,
            booking__showtime_id=showtime_id
        ).exists()


class BookingSerializer(serializers.ModelSerializer):
    seats = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    showtime_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ('id', 'showtime_id', 'seats')

    def create(self, validated_data):
        user = self.context['request'].user
        showtime_id = validated_data.pop('showtime_id')
        showtime = Showtime.objects.get(id=showtime_id)
        seat_ids = validated_data.pop('seats')

        booked_seats_qs = BookedSeat.objects.filter(
            booking__showtime=showtime,
            seat_id__in=seat_ids
        )
        if booked_seats_qs.exists():
            raise serializers.ValidationError("One or more selected seats are already booked.")

        booking = Booking.objects.create(user=user, showtime=showtime)
        for seat_id in seat_ids:
            seat = Seat.objects.get(id=seat_id)
            BookedSeat.objects.create(booking=booking, seat=seat)

        return booking