from rest_framework import serializers
from .models import Movie, Genre, Rating


# ---------------------------------------
#  Genre Serializer
# ---------------------------------------
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


# ---------------------------------------
#  Rating Serializer (nested inside Movie)
# ---------------------------------------
class RatingSerializer(serializers.ModelSerializer):
    """
    Used inside MovieSerializer
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'rating', 'created_at']  # ✅ FIXED


# ---------------------------------------
#  Movie Serializer
# ---------------------------------------
class MovieSerializer(serializers.ModelSerializer):

    genres = GenreSerializer(many=True, read_only=True)

    # DB → API rename
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

    # ---------------------------------------
    #  Current user's rating
    # ---------------------------------------
    def get_your_rating(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            rating = obj.ratings.filter(user=user).first()
            return rating.rating if rating else None   # ✅ FIXED

        return None

    # ---------------------------------------
    #  Lightweight recommendations
    # ---------------------------------------
    def get_recommendations(self, obj):
        from random import sample

        ids = list(
            Movie.objects.exclude(id=obj.id)
            .values_list('id', flat=True)
        )

        if not ids:
            return []

        sample_ids = sample(ids, min(3, len(ids)))

        recs = Movie.objects.filter(id__in=sample_ids).only(
            'id', 'title', 'poster_url', 'average_rating'
        )

        return [
            {
                'id': m.id,
                'title': m.title,
                'poster_url': m.poster_url,
                'avg_rating': m.average_rating
            }
            for m in recs
        ]