from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster_image = models.ImageField(upload_to='posters/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='heros/', blank=True, null=True)
    duration = models.IntegerField()
    genre = models.CharField(max_length=200)
    trailer_urls = models.URLField()
    release_date = models.DateField()

    def __str__(self):
        return self.title