from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.pagination import PageNumberPagination


class MoviePagination(PageNumberPagination):
    page_size = 5


class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()

        search = request.GET.get('search')
        if search:
            movies = movies.filter(title__icontains=search)

        genre = request.GET.get('genre')
        if genre:
            movies = movies.filter(genres__name__icontains=genre)

        paginator = MoviePagination()
        paginated_movies = paginator.paginate_queryset(movies, request)

        serializer = MovieSerializer(paginated_movies, many=True)
        return paginator.get_paginated_response(serializer.data)

class MovieDetailView(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response(
                {"error": "Movie not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MovieSerializer(movie)
        return Response(serializer.data)

class TrendingMoviesView(APIView):
    def get(self, request):
        movies = Movie.objects.order_by('-average_rating')[:10]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)