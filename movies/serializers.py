from rest_framework import serializers
from .models import Movie, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    avg_rating = serializers.FloatField(read_only=True)
    num_ratings = serializers.IntegerField(read_only=True)
    url = serializers.CharField(read_only=True)      # watch link
    image = serializers.ImageField(read_only=True)   # poster image

    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'description',
            'release_year',
            'genres',
            'avg_rating',
            'num_ratings',
            'url',
            'image',
        ]