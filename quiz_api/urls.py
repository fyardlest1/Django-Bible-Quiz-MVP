from django.urls import path
from .views import (
    DailyQuizView, 
    SubmitQuizView, 
    CategoryListView, 
    QuizPackQuestionsView,
    UserStatsView,
    RecentAttemptsView, 
    LeaderboardView,
    SubscribeView # Import the new view
)

urlpatterns = [
    # Feature 1: Daily Random Quiz
    path('daily-quiz/', DailyQuizView.as_view(), name='daily-quiz'),
    path('submit-answers/', SubmitQuizView.as_view(), name='submit-answers'),

    # Feature 2: Category Packs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('quizzes/<slug:category_slug>/', QuizPackQuestionsView.as_view(), name='quiz-pack-questions'),
    
    # Feature 3: Progress Tracking (Active)
    path('stats/', UserStatsView.as_view(), name='user-stats'),
    path('attempts/recent/', RecentAttemptsView.as_view(), name='recent-attempts'),
    
    # Feature 5: Leaderboard
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard-list'),
    
    # Feature 6: Daily Email Reminders
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]