from django.urls import path
from .views import MovieListView, MovieDetailView, TrendingMoviesView, SubmitRatingView

urlpatterns = [
    path('trending/', TrendingMoviesView.as_view(), name='trending-movies'),
    path('<int:movie_id>/rate/', SubmitRatingView.as_view(), name='submit-rating'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movies-detail'),
    path('', MovieListView.as_view(), name='movies-list'),
]