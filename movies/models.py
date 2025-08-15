from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster_image = models.URLField(max_length=500, blank=True)
    duration = models.IntegerField()
    genre = models.CharField(max_length=200)
    release_date = models.DateField()

    def __str__(self):
        return self.title