from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg

from .models import Rating
from .serializers import RatingSerializer
from movies.models import Movie


class RatingCreateView(APIView):
    def post(self, request):
        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            rating = serializer.save(user=request.user)

            movie = rating.movie

            avg_rating = movie.ratings.aggregate(
                avg=Avg('value')
            )['avg']

            movie.average_rating = round(avg_rating, 2) if avg_rating else None
            movie.save(update_fields=["average_rating"])

            return Response({
                "message": "Rating added successfully",
                "new_average": movie.average_rating
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)