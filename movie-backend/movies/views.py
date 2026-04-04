from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Q, Value
from django.db.models.functions import Coalesce
from rest_framework.pagination import PageNumberPagination
from .models import Movie, Rating
from .serializers import MovieSerializer


class MoviePagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    pagination_class = MoviePagination

    def get_queryset(self):
        # Always order by average_rating desc, then title for consistent pagination
        qs = Movie.objects.all().order_by('-average_rating', 'title')
        query = self.request.query_params.get('search')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(genres__name__icontains=query)
            ).distinct()
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]


@method_decorator(cache_page(60 * 10), name='dispatch')
class TrendingMoviesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        trending = Movie.objects.annotate(
            safe_rating=Coalesce('average_rating', Value(0.0))
        ).order_by('-safe_rating', 'title')[:5]  # secondary ordering

        serializer = MovieSerializer(trending, many=True, context={'request': request})
        return Response(serializer.data)


class SubmitRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            value = int(request.data.get('rating'))
        except (TypeError, ValueError):
            return Response({'error': 'Invalid rating value'}, status=status.HTTP_400_BAD_REQUEST)

        if not 1 <= value <= 5:
            return Response({'error': 'Rating must be 1-5'}, status=status.HTTP_400_BAD_REQUEST)

        Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'value': value}
        )
        movie.update_average_rating()

        serializer = MovieSerializer(movie, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)