from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class CinemaHall(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.IntegerField(default=50)

    def __str__(self):
        return self.name

class Showtime(models.Model):
    movie =models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='showtimes')
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.hall.title} on {self.show_time.strftime('%Y-%m-%d %H:%M')}"

class Seat(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='seats')
    seat_row = models.CharField(max_length=1)
    seat_number = models.IntegerField()

    class Meta:
        unique_together = ('hall', 'seat_row', 'seat_number')

    def __str__(self):
        return f"Seat {self.seat_row}{self.seat_number} in {self.hall.name}"

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