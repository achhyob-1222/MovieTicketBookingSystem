from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


class CinemaHall(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.IntegerField(default=50)

    def __str__(self):
        return self.name


class Showtime(models.Model):
    # These choices are now just for reference within the model's logic
    HALL_A_TIMES = [datetime.time(6, 0), datetime.time(13, 0), datetime.time(20, 0)]
    HALL_B_TIMES = [datetime.time(8, 0), datetime.time(13, 0), datetime.time(18, 0)]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()  # This is now a standard time field

    def __str__(self):
        return f"{self.movie.title} in {self.hall.name} on {self.date} at {self.time.strftime('%I:%M %p')}"

    def clean(self):
        # Prevent scheduling a movie in the past
        if self.date < timezone.now().date():
            raise ValidationError("Cannot schedule a showtime for a past date.")

        # Prevent scheduling two movies in the same hall at the same date and time
        conflicting_showtimes = Showtime.objects.filter(
            hall=self.hall,
            date=self.date,
            time=self.time
        ).exclude(pk=self.pk)

        if conflicting_showtimes.exists():
            raise ValidationError(f"A showtime already exists in {self.hall.name} at this date and time.")

        # NEW VALIDATION: Check if the selected time is valid for the selected hall
        if self.hall.name == 'Hall A' and self.time not in self.HALL_A_TIMES:
            raise ValidationError("Invalid time for Hall A. Valid times are 6:00 AM, 1:00 PM, 8:00 PM.")
        elif self.hall.name == 'Hall B' and self.time not in self.HALL_B_TIMES:
            raise ValidationError("Invalid time for Hall B. Valid times are 8:00 AM, 1:00 PM, 6:00 PM.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Seat(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='seats')
    seat_row = models.CharField(max_length=1)
    seat_number = models.IntegerField()

    class Meta:
        unique_together = ('hall', 'seat_row', 'seat_number')

    def __str__(self):
        return f"Seat {self.seat_row}{self.seat_number} in {self.hall.name}"


# --- (Booking and BookedSeat models remain the same) ---
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='bookings')
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.showtime.movie.title}"


class BookedSeat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booked_seats')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('booking', 'seat')

    def __str__(self):
        return f"{self.seat} for booking {self.booking.id}"