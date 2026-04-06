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

        # --------------------------------------------------
        # Get all movie IDs rated by the current user
        # This ensures we NEVER recommend already rated movies
        # --------------------------------------------------

        print("USER:", request.user)
        print("AUTH:", request.user.is_authenticated)
        if request.user.is_authenticated:
            rated_ids_debug = list(
        Rating.objects.filter(user=request.user).values_list('movie_id', flat=True))
        else:
            rated_ids_debug = []

        print("RATED IDS:", rated_ids_debug)
        if user.is_authenticated:
            rated_movie_ids = list(
                Rating.objects.filter(user=user)
                .values_list('movie_id', flat=True)
            )
        else:
            rated_movie_ids = []

        # --------------------------------------------------
        # Get genres from movies the user liked (rating >= 4)
        # Used for personalized recommendations
        # --------------------------------------------------
        if user.is_authenticated:
            liked_genre_ids = set(
                Rating.objects.filter(user=user, value__gte=4)
                .values_list('movie__genres__id', flat=True)
            )
        else:
            liked_genre_ids = set()

        # --------------------------------------------------
        # Fallback: If user has no strong preferences
        # Return popular movies (most rated + highest rated)
        # --------------------------------------------------
        if not liked_genre_ids:
            fallback_movies = (
                Movie.objects
                .annotate(
                    avg_rating=Avg('ratings__value'),
                    num_ratings=Count('ratings')
                )
                .exclude(id__in=rated_movie_ids)  # avoid already rated movies
                .order_by('-num_ratings', '-avg_rating')[:10]
            )

            serializer = MovieSerializer(
                fallback_movies,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)

        # --------------------------------------------------
        # Personalized recommendations
        # Filter movies by liked genres and exclude rated ones
        # --------------------------------------------------
        movies = (
            Movie.objects
            .annotate(
                avg_rating=Avg('ratings__value'),
                num_ratings=Count('ratings')
            )
            .filter(genres__id__in=liked_genre_ids)
            .exclude(id__in=rated_movie_ids)
            .distinct()
            .prefetch_related('genres')
        )

        # Extra safety: ensure no rated movie slips through
        movies = [m for m in movies if m.id not in rated_movie_ids]

        # --------------------------------------------------
        # Score movies using hybrid logic:
        # genre match + average rating + popularity
        # --------------------------------------------------
        movie_scores = []

        for movie in movies:
            movie_genre_ids = {g.id for g in movie.genres.all()}
            genre_match_count = len(movie_genre_ids & liked_genre_ids)

            score = (
                genre_match_count * 0.5 +
                (movie.avg_rating or 0) * 0.3 +
                (movie.num_ratings or 0) * 0.2
            )

            movie_scores.append((score, movie))

        # Sort by score and pick top 10
        top_movies = [
            movie for score, movie in sorted(
                movie_scores,
                key=lambda x: x[0],
                reverse=True
            )
        ][:10]

        serializer = MovieSerializer(
            top_movies,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)