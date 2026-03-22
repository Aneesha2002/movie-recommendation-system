from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from .models import Movie
from .serializers import MovieSerializer

# List all movies (raw array, no pagination)
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = None  # return raw list for Angular

# Get movie by ID
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class TrendingMoviesView(APIView):
    def get(self, request):
        trending = Movie.objects.order_by('-rating')[:5]  # use existing rating field
        serializer = MovieSerializer(trending, many=True)
        return Response(serializer.data)