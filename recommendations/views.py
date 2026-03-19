from rest_framework.views import APIView
from rest_framework.response import Response
from ratings.models import Rating
from movies.models import Movie
from movies.serializers import MovieSerializer


class RecommendationView(APIView):
    def get(self, request, user_id):

        # Step 1: Get user ratings
        user_ratings = Rating.objects.filter(user_id=user_id)

        # Step 2: Build weighted genre preference
        genre_scores = {}

        for rating in user_ratings:
            for genre in rating.movie.genres.all():
                genre_scores[genre.id] = genre_scores.get(genre.id, 0) + rating.rating

        # Step 3: Get all movies
        movies = Movie.objects.all()

        # Step 4: Score movies
        scored_movies = []

        rated_movie_ids = user_ratings.values_list('movie_id', flat=True)

        for movie in movies:
            if movie.id in rated_movie_ids:
                continue

        score = 0

        for genre in movie.genres.all():
            score += genre_scores.get(genre.id, 0)

        score += movie.average_rating * 2

        if score > 0:
            scored_movies.append((movie, score))

        # Step 5: Sort by score
        scored_movies.sort(key=lambda x: x[1], reverse=True)

        top_movies = [movie for movie, score in scored_movies[:10]]

        serializer = MovieSerializer(top_movies, many=True)
        return Response(serializer.data)