from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "quiz_ui/home.html"


class QuizView(TemplateView):
    template_name = "quiz_ui/quiz.html"


class LeaderboardView(TemplateView):
    template_name = "quiz_ui/leaderboard.html"