from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from movies.models import Movie, Rating
from django.db.models import Count, Avg


class RecommendationView(APIView):
    """
    Public endpoint for movie recommendations.

    Works for:
    - Logged-in users → personalized recommendations
    - Anonymous users → fallback (top-rated / popular movies)
    """
    permission_classes = [AllowAny]  # Public access

    def get(self, request):
        user = request.user

        # ---------------------------------------
        # 1. Get user's ratings (if logged in)
        # ---------------------------------------
        if user.is_authenticated:
            user_ratings = Rating.objects.filter(user=user)
        else:
            user_ratings = Rating.objects.none()

        # Movies the user liked (rating >= 4)
        liked_movies = user_ratings.filter(value__gte=4)

        # ---------------------------------------
        # 2. Get liked genres (OPTIMIZED)
        # ---------------------------------------
        liked_genre_ids = set(
            Movie.objects.filter(
                ratings__user=user,
                ratings__value__gte=4
            ).values_list('genres__id', flat=True)
        ) if user.is_authenticated else set()

        # ---------------------------------------
        # 3. Fallback for new / anonymous users
        # ---------------------------------------
        if not liked_genre_ids:
            # Return top movies based on popularity + rating
            fallback_movies = Movie.objects.annotate(
                avg_rating=Avg('ratings__value'),
                num_ratings=Count('ratings')
            ).order_by('-num_ratings', '-avg_rating')[:10]

            return Response([
                {
                    "id": m.id,
                    "title": m.title,
                    "poster_url": m.poster_url,
                    "avg_rating": round(m.avg_rating or 0, 2)
                }
                for m in fallback_movies
            ])

        # ---------------------------------------
        # 4. Exclude already rated movies
        # ---------------------------------------
        rated_movie_ids = user_ratings.values_list('movie_id', flat=True)

        # ---------------------------------------
        # 5. Get candidate movies
        # ---------------------------------------
        movies = Movie.objects.annotate(
            avg_rating=Avg('ratings__value'),
            num_ratings=Count('ratings')
        ).filter(
            genres__id__in=liked_genre_ids
        ).exclude(
            id__in=rated_movie_ids
        ).distinct().prefetch_related('genres')[:50]

        # ---------------------------------------
        # 6. Score movies (hybrid recommendation)
        # ---------------------------------------
        movie_scores = []

        for movie in movies:
            movie_genre_ids = {g.id for g in movie.genres.all()}

            # How many genres match user's preferences
            genre_match_count = len(movie_genre_ids & liked_genre_ids)

            # Hybrid score formula
            score = (
                genre_match_count * 0.5 +          # genre similarity
                (movie.avg_rating or 0) * 0.3 +    # quality
                (movie.num_ratings or 0) * 0.2     # popularity
            )

            movie_scores.append((score, movie))

        # ---------------------------------------
        # 7. Get top 10 movies
        # ---------------------------------------
        top_movies = [
            m for s, m in sorted(movie_scores, key=lambda x: x[0], reverse=True)
        ][:10]

        # ---------------------------------------
        # 8. Final response
        # ---------------------------------------
        return Response([
            {
                "id": m.id,
                "title": m.title,
                "poster_url": m.poster_url,
                "avg_rating": round(m.avg_rating or 0, 2)
            }
            for m in top_movies
        ])