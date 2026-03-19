from django.urls import path
from .views import MovieListView, MovieDetailView,TrendingMoviesView

urlpatterns = [
    path('', MovieListView.as_view()),
    path('trending/', TrendingMoviesView.as_view()),
    path('<int:pk>/', MovieDetailView.as_view()),
]