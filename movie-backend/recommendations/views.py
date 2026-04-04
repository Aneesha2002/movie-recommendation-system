from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from movies.models import Movie, Rating
from movies.serializers import MovieSerializer
from django.db.models import Count, Avg

class RecommendationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        user_ratings = Rating.objects.filter(user=user) if user.is_authenticated else Rating.objects.none()
        liked_genre_ids = set(
            Movie.objects.filter(ratings__user=user, ratings__value__gte=4).values_list('genres__id', flat=True)
        ) if user.is_authenticated else set()

        if not liked_genre_ids:
            fallback_movies = Movie.objects.annotate(
                avg_rating=Avg('ratings__value'),
                num_ratings=Count('ratings')
            ).order_by('-num_ratings', '-avg_rating')[:10]
            serializer = MovieSerializer(fallback_movies, many=True, context={'request': request})
            return Response(serializer.data)

        rated_movie_ids = list(user_ratings.values_list('movie_id', flat=True))
        movies = Movie.objects.exclude(
        id__in=rated_movie_ids
        ).annotate(
        avg_rating=Avg('ratings__value'),
        num_ratings=Count('ratings')
        ).filter(
        genres__id__in=liked_genre_ids
        ).distinct().prefetch_related('genres')[:50]

        # Score movies by hybrid method
        movie_scores = []
        for movie in movies:
            movie_genre_ids = {g.id for g in movie.genres.all()}
            genre_match_count = len(movie_genre_ids & liked_genre_ids)
            score = genre_match_count * 0.5 + (movie.avg_rating or 0) * 0.3 + (movie.num_ratings or 0) * 0.2
            movie_scores.append((score, movie))

        top_movies = [m for s, m in sorted(movie_scores, key=lambda x: x[0], reverse=True)][:10]
        serializer = MovieSerializer(top_movies, many=True, context={'request': request})
        return Response(serializer.data)