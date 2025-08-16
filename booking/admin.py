from django.contrib import admin
from booking.models import CinemaHall, Showtime, Seat, Booking, BookedSeat

# Register your models here.
admin.site.register(Booking)
admin.site.register(CinemaHall)
admin.site.register(BookedSeat)
admin.site.register(Showtime)
admin.site.register(Seat)

