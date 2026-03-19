from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_year = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='movies')
    average_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title