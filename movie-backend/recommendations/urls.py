from django.urls import path
from .views import RecommendationView

urlpatterns = [
    path('<int:user_id>/', RecommendationView.as_view()),
]