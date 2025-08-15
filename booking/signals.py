from django.db.models.signals import post_save
from django.dispatch import receiver
from movies.models import Movie
from .models import CinemaHall, Showtime, Seat
from datetime import datetime, time


@receiver(post_save, sender=Movie)
def create_daily_showtimes(sender, instance, created, **kwargs):
    # This function runs every time a new movie is created
    if created:
        # Get or create our two cinema halls
        hall1, _ = CinemaHall.objects.get_or_create(name='Hall 1', defaults={'total_seats': 50})
        hall2, _ = CinemaHall.objects.get_or_create(name='Hall 2', defaults={'total_seats': 50})

        # Automatically create seats for the halls if they don't have any
        if not hall1.seats.exists():
            for row in ['A', 'B', 'C', 'D', 'E']:
                for num in range(1, 11):
                    Seat.objects.create(hall=hall1, seat_row=row, seat_number=num)

        if not hall2.seats.exists():
            for row in ['A', 'B', 'C', 'D', 'E']:
                for num in range(1, 11):
                    Seat.objects.create(hall=hall2, seat_row=row, seat_number=num)

        # Define the showtimes for today
        today = datetime.now().date()
        show_times_hall1 = [time(8, 0), time(16, 0)]  # 8:00 AM and 4:00 PM
        show_times_hall2 = [time(11, 0), time(18, 0)]  # 11:00 AM and 6:00 PM

        for show_time in show_times_hall1:
            Showtime.objects.create(
                movie=instance,
                hall=hall1,
                show_time=datetime.combine(today, show_time)
            )

        for show_time in show_times_hall2:
            Showtime.objects.create(
                movie=instance,
                hall=hall2,
                show_time=datetime.combine(today, show_time)
            )