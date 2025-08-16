from django.contrib import admin
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date')

admin.site.register(Movie, MovieAdmin)
