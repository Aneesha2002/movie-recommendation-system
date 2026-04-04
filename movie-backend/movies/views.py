from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Q

from .models import Movie, Rating
from .serializers import MovieSerializer

# -------------------------------
# Public: List Movies (with search)
# -------------------------------
class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]  
    pagination_class = None  

    def get_queryset(self):
        qs = Movie.objects.all()

        # Search by title, description, or genre
        query = self.request.query_params.get('search')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(genres__name__icontains=query)
            ).distinct()

        return qs

    def get_serializer_context(self):
        """
        Pass request to serializer.
        Needed for 'your_rating' field to work per user.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# -------------------------------
# Public: Movie Details
# -------------------------------
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny] 


# -------------------------------
# Public: Trending Movies (cached)
# -------------------------------
@method_decorator(cache_page(60 * 10), name='dispatch')
class TrendingMoviesView(APIView):
    permission_classes = [AllowAny]  # ✅ Public

    def get(self, request):
        """
        Returns top 5 movies sorted by average rating.
        Cached for 10 minutes to reduce DB load.
        """
        trending = Movie.objects.order_by('-average_rating')[:5]
        serializer = MovieSerializer(
            trending,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


# -------------------------------
# Protected: Submit Rating
# -------------------------------
class SubmitRatingView(APIView):
    permission_classes = [IsAuthenticated]  # Login required

    def post(self, request, movie_id):
        """
        Create or update a user's rating for a movie.
        Only logged-in users can rate.
        """

        # Validate movie exists
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response(
                {'error': 'Movie not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate rating input
        try:
            value = int(request.data.get('rating'))
        except (TypeError, ValueError):
            return Response(
                {'error': 'Invalid rating value'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if value < 1 or value > 5:
            return Response(
                {'error': 'Rating must be between 1 and 5'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update or create rating (one rating per user per movie)
        rating, created = Rating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'value': value}
        )

        # Recalculate average rating
        movie.update_average_rating()

        return Response(
            {
                'message': 'Rating submitted successfully',
                'avg_rating': movie.average_rating
            },
            status=status.HTTP_200_OK
        )