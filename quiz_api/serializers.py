from rest_framework import serializers
from .models import Question, QuizAttempt, Category, LeaderboardEntry

# --- Core MVP Serializers ---

class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying questions in the daily quiz.
    Note: It EXCLUDES the 'correct_answer' and 'explanation' fields.
    """
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Question
        # Exclude sensitive fields from the quiz delivery API
        fields = ('id', 'question_text', 'choices', 'category_display')
        read_only_fields = fields


class AnswerSubmissionSerializer(serializers.Serializer):
    """
    Validates the user's answer submission.
    UPGRADE: Accepts 'group_id' to link attempts to a specific church/group leaderboard.
    """
    question_id = serializers.IntegerField()
    selected_answer = serializers.CharField(max_length=255)
    
    # Optional: For tracking user history anonymously
    device_id = serializers.CharField(max_length=255, required=False, allow_blank=True)
    
    # NEW: Optional Group ID for church/youth group leaderboards (Feature 5)
    group_id = serializers.CharField(max_length=100, required=False, allow_blank=True)


class QuizAttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for the QuizAttempt result object.
    """
    class Meta:
        model = QuizAttempt
        fields = '__all__'


# --- Feature 3: New Serializer for Stats ---

class UserStatsSerializer(serializers.Serializer):
    """
    Detailed progress tracking for the frontend 'Profile' or 'Stats' screen.
    UPGRADE: Includes Streak and Category breakdown.
    """
    total_quizzes = serializers.IntegerField()
    total_score = serializers.IntegerField()
    average_score = serializers.FloatField()
    last_played = serializers.DateTimeField(allow_null=True)
    
    # NEW: Engagement metrics (Feature 3)
    current_streak = serializers.IntegerField()
    
    # NEW: A dictionary showing performance/activity (e.g., {'GTV': 50, 'WST': 80})
    category_breakdown = serializers.DictField()


# --- Scaffold Serializers ---

class CategorySerializer(serializers.ModelSerializer):
    """
    Simple serializer for listing available quiz packs.
    """
    class Meta:
        model = Category
        fields = '__all__'


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    """
    Legacy serializer for the LeaderboardEntry model (mostly deprecated by real-time aggregation).
    """
    class Meta:
        model = LeaderboardEntry
        fields = '__all__'