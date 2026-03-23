from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer

# Movies list with search
@method_decorator(cache_page(60 * 10), name='dispatch')
class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Movie.objects.all()
        query = self.request.query_params.get('search')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(genres__name__icontains=query)
            ).distinct()
        return qs

    def get_serializer_context(self):
        # Pass the request so your MovieSerializer can return your_rating correctly
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# Movie details
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# Trending movies by average rating
@method_decorator(cache_page(60 * 10), name='dispatch')
class TrendingMoviesView(APIView):
    def get(self, request):
        trending = Movie.objects.order_by('-average_rating')[:5]
        serializer = MovieSerializer(trending, many=True, context={'request': request})
        return Response(serializer.data)

class SubmitRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        # Accept 'rating' from frontend
        try:
            value = int(request.data.get('rating'))
        except (TypeError, ValueError):
            return Response({'error': 'Invalid rating value'}, status=status.HTTP_400_BAD_REQUEST)

        if value < 1 or value > 5:
            return Response({'error': 'Rating must be 1-5'}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'value': value}
        )

        movie.update_average_rating()

        return Response({
            'message': 'Rating submitted successfully',
            'avg_rating': movie.average_rating
        }, status=status.HTTP_200_OK)