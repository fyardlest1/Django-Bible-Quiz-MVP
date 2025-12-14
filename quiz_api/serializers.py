from rest_framework import serializers

from .models import (
    Question, QuizAttempt, 
    Category, LeaderboardEntry, 
    DailyReminderSubscriber, StudyGroup
)

from .tasks import send_day1_email

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

# --- UPDATED: Subscriber Serializer ---

class SubscriberSerializer(serializers.ModelSerializer):
    """
    Handles email subscription and links anonymous progress.
    """
    # Write-only field for the anonymous session ID
    device_id = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = DailyReminderSubscriber
        fields = ['email', 'device_id']

    def create(self, validated_data):
        email = validated_data['email']
        device_id = validated_data.pop('device_id', None)
        
        # 1. Create or Reactivate Subscriber
        subscriber, created = DailyReminderSubscriber.objects.get_or_create(email=email)
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            
        # 2. Look up current streak from anonymous session (QuizAttempt)
        streak = 0
        if device_id:
            last_attempt = QuizAttempt.objects.filter(device_id=device_id).order_by('-timestamp').first()
            if last_attempt:
                streak = last_attempt.current_streak
        
        # 3. Persist the streak to the permanent subscriber record
        # Only update if the new streak is higher or if establishing for the first time
        if streak > subscriber.current_streak:
            subscriber.current_streak = streak
            
        subscriber.save()
        
        # 4. Trigger Welcome Email (Async Task)
        # UPDATED: Calling send_day1_email which includes the PDF link and DB logging
        send_day1_email.delay(email, subscriber.current_streak)
            
        return subscriber

# --- NEW: Study Group Serializer ---

class StudyGroupSerializer(serializers.ModelSerializer):
    invite_link = serializers.SerializerMethodField()
    member_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'group_code', 'invite_link', 'member_count']
        read_only_fields = ['id', 'group_code', 'invite_link', 'member_count']

    def get_invite_link(self, obj):
        # Dynamically build the link. 
        # For this MVP, we assume the frontend root URL structure /play/?group_id=...
        return f"/play/?group_id={obj.group_code}"
