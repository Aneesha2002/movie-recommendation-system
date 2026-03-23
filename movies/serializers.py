from rest_framework import serializers
from .models import Movie, Genre, Rating

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'value', 'created_at', 'updated_at']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    avg_rating = serializers.FloatField(source='average_rating', read_only=True)
    your_rating = serializers.SerializerMethodField()
    recommendations = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'release_year',
            'genres', 'poster_url', 'avg_rating', 'your_rating',
            'recommendations'
        ]

    def get_your_rating(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            rating = obj.ratings.filter(user=user).first()
            return rating.value if rating else 0
        return 0

    def get_recommendations(self, obj):
        # Avoid recursion: do not include recommendations of recommendations
        from random import sample
        qs = Movie.objects.exclude(id=obj.id)
        recs = sample(list(qs), min(3, qs.count())) if qs.exists() else []
        # Only basic serializer to prevent infinite recursion
        return [
            {
                'id': m.id,
                'title': m.title,
                'poster_url': m.poster_url,
                'avg_rating': m.average_rating
            } for m in recs
        ]