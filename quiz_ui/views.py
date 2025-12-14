from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "quiz_ui/home.html"


class QuizView(TemplateView):
    template_name = "quiz_ui/quiz.html"


class LeaderboardView(TemplateView):
    template_name = "quiz_ui/leaderboard.html"


class TeacherModeView(TemplateView):
    template_name = "quiz_ui/teacher_mode.html"


class RegisterView(TemplateView):
    template_name = "quiz_ui/register.html"


class CreateGroupView(TemplateView):
    template_name = "quiz_ui/create_group.html"

