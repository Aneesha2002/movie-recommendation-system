from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

from .models import Rating
from .serializers import RatingSerializer
from movies.models import Movie


class RatingCreateView(APIView):
    permission_classes = [IsAuthenticated]  # require login

    def post(self, request):
        movie_id = request.data.get("movie")

        # basic validation
        if not movie_id:
            return Response(
                {"error": "Movie ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(
                {"error": "Movie not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            value = int(request.data.get("value"))
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid rating value"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if value < 1 or value > 5:
            return Response(
                {"error": "Rating must be between 1 and 5"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # update or create rating
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={"value": value}
        )

        # recalculate average
        avg_rating = movie.ratings.aggregate(avg=Avg('value'))['avg']
        movie.average_rating = round(avg_rating, 2) if avg_rating else None
        movie.save(update_fields=["average_rating"])

        return Response({
            "message": "Rating updated" if not created else "Rating added",
            "avg_rating": movie.average_rating
        }, status=status.HTTP_200_OK)