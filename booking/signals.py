from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CinemaHall, Seat


@receiver(post_migrate)
def setup_halls_and_seats(sender, **kwargs):
    # This signal now only runs once to set up the initial halls and seats.
    if sender.name == 'booking' and CinemaHall.objects.count() == 0:
        print("No cinema halls found. Creating initial halls and seats...")

        hall_a = CinemaHall.objects.create(name='Hall A', total_seats=50)
        for row in ['A', 'B', 'C', 'D', 'E']:
            for num in range(1, 11):
                Seat.objects.create(hall=hall_a, seat_row=row, seat_number=num)

        hall_b = CinemaHall.objects.create(name='Hall B', total_seats=50)
        for row in ['A', 'B', 'C', 'D', 'E']:
            for num in range(1, 11):
                Seat.objects.create(hall=hall_b, seat_row=row, seat_number=num)

        print("Initial halls and seats created successfully.")