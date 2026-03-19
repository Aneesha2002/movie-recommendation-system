from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Rating
from .serializers import RatingSerializer
from django.db.models import Avg
from movies.models import Movie


class RatingCreateView(APIView):
    def post(self, request):
        serializer = RatingSerializer(data=request.data)

        if serializer.is_valid():
            rating = serializer.save()

            # Update average rating
            movie = rating.movie
            avg_rating = movie.rating_set.aggregate(Avg('rating'))['rating__avg']
            movie.average_rating = avg_rating
            movie.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)