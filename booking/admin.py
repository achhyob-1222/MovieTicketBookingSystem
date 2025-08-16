from django.contrib import admin
from booking.models import CinemaHall, Showtime, Seat, Booking, BookedSeat
from django import forms


class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'date', 'time')
    list_filter = ('date', 'hall', 'movie')

    # Add a help text to guide the user
    fieldsets = (
        (None, {
            'fields': ('movie', 'hall', 'date', 'time'),
            'description': "For Hall A, valid times are 06:00, 13:00, 20:00. For Hall B, valid times are 08:00, 13:00, 18:00."
        }),
    )


admin.site.register(CinemaHall)
admin.site.register(Showtime, ShowtimeAdmin)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(BookedSeat)


