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
            rating = serializer.save()

            movie = rating.movie

            avg_rating = movie.ratings.aggregate(Avg('rating'))['rating__avg']

            movie.rating = avg_rating
            movie.save(update_fields=["rating"])

            return Response({
                "message": "Rating added successfully",
                "new_average": avg_rating
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)