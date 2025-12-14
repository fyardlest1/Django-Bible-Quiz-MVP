from django.urls import path
from .views import (
    HomeView, QuizView, 
    LeaderboardView, TeacherModeView, 
    RegisterView, CreateGroupView
)


app_name = 'quiz_ui'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('play/', QuizView.as_view(), name='play'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('teacher-mode/', TeacherModeView.as_view(), name='teacher_mode'),
    path('register/', RegisterView.as_view(), name='register'),
    path('groups/create/', CreateGroupView.as_view(), name='create_group'),
]