# movies/serializers.py
from rest_framework import serializers
from .models import Movie, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    avg_rating = serializers.FloatField(read_only=True)
   

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_year', 'genres', 'avg_rating']