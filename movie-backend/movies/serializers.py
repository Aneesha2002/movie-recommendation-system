from rest_framework import serializers
from .models import Movie, Genre, Rating
from random import sample  # move import to top-level

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'value', 'created_at']  # use 'value' instead of 'rating'


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(source='average_rating', read_only=True)
    your_rating = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_year',
            'genres', 'poster_url', 'avg_rating',
            'your_rating', 'recommendations', 'ratings'
        ]

    def get_your_rating(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            rating = obj.ratings.filter(user=user).first()
            return rating.value if rating else None
        return None

    def get_recommendations(self, obj):
        ids = list(Movie.objects.exclude(id=obj.id).values_list('id', flat=True))
        if not ids:
            return []  # safe if no other movies
        sample_ids = sample(ids, min(3, len(ids)))
        recs = Movie.objects.filter(id__in=sample_ids).values(
            'id', 'title', 'poster_url', 'average_rating'
        )
        return list(recs)