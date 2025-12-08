from django.urls import path
from .views import HomeView, QuizView, LeaderboardView


app_name = 'quiz_ui'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('play/', QuizView.as_view(), name='play'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]