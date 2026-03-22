from rest_framework.views import APIView
from rest_framework.response import Response
from movies.models import Movie
from ratings.models import Rating
from django.db.models import Count, Avg

class RecommendationView(APIView):
    def get(self, request, user_id):
        # Get user ratings
        user_ratings = Rating.objects.filter(user_id=user_id)
        liked_movies = user_ratings.filter(rating__gte=4)

        # Get genres from liked movies
        liked_genre_ids = []
        for rating in liked_movies:
            liked_genre_ids.extend([g.id for g in rating.movie.genres.all()])

        # Already rated movies
        rated_movie_ids = user_ratings.values_list('movie_id', flat=True)

        # Candidate movies
        movies = Movie.objects.annotate(
            avg_rating=Avg('rating__rating'),
            num_ratings=Count('rating')
        ).filter(
            genres__id__in=liked_genre_ids
        ).exclude(
            id__in=rated_movie_ids
        ).distinct()

        # Simple hybrid scoring: genre + popularity + avg_rating
        movie_scores = []
        for movie in movies:
            genre_match_count = len(set([g.id for g in movie.genres.all()]) & set(liked_genre_ids))
            score = genre_match_count * 0.5 + (movie.avg_rating or 0) * 0.3 + movie.num_ratings * 0.2
            movie_scores.append((score, movie))

        # Sort by score descending
        top_movies = [m for s, m in sorted(movie_scores, key=lambda x: x[0], reverse=True)][:10]

        data = [{"id": m.id, "title": m.title} for m in top_movies]
        return Response(data)

class TrendingMoviesView(APIView):
    def get(self, request):
        # Top 5 movies with most ratings
        movies = Movie.objects.annotate(
            num_ratings=Count('rating'),
            avg_rating=Avg('rating__rating')
        ).order_by('-num_ratings', '-avg_rating')[:5]

        data = [
            {
                "id": movie.id,
                "title": movie.title,
                "num_ratings": movie.num_ratings,
                "avg_rating": round(movie.avg_rating or 0, 2)
            }
            for movie in movies
        ]
        return Response(data)