from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_year = models.IntegerField()
    language = models.CharField(max_length=10, default='en-US')
    genres = models.ManyToManyField(Genre, related_name='movies')
    average_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    poster_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            self.average_rating = round(sum(r.value for r in ratings) / ratings.count(), 2)
        else:
            self.average_rating = 0.0
        self.save()


class Rating(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='movie_ratings'  # <-- unique related_name to avoid clash
    )
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE, 
        related_name='ratings'  # keeps your existing movie->ratings relationship
    )
    value = models.PositiveSmallIntegerField()  # 1-5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.value}"