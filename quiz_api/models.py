from django.db import models
from django.contrib.postgres.fields import ArrayField # Use ArrayField for simple list of choices, but standard Django choice for category
from django.utils.crypto import get_random_string

# Define category choices for the Question model
CATEGORY_CHOICES = [
    ('GTV', 'Guess the Verse'),
    ('WST', 'Who Said This?'),
    ('ONT', 'Old or New Testament'),
]

class Category(models.Model):
    """
    Model for managing quiz categories (e.g., 'Prophets', 'Parables').
    """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    The core question model.
    Includes the explanation field for Feature 4 (Instant Learning).
    """
    question_text = models.TextField()
    # Storing choices as a simple JSON/Text field for MVP simplicity
    choices = models.JSONField(
        help_text="A list of 3-4 string choices, e.g., ['A', 'B', 'C', 'D']"
    )
    correct_answer = models.CharField(max_length=255)
    
    # Use the defined choices for the MVP category types
    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        default='GTV'
    )
    explanation = models.TextField(blank=True, null=True) # Feature 4: Instant Explanations

    def __str__(self):
        return f"[{self.get_category_display()}] {self.question_text[:50]}..."


class QuizAttempt(models.Model):
    """
    Tracks user progress. 
    UPGRADE: Includes Streak Logic and Group IDs for church leaderboards.
    """
    # Used for anonymous user tracking (e.g. UUID from frontend)
    device_id = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    
    # NEW (Feature 5): Allow users to join a 'board' or 'group' (e.g., 'YouthGroup1')
    # Indexed because we will filter by this frequently for custom leaderboards
    group_id = models.CharField(max_length=100, db_index=True, blank=True, null=True)
    
    score = models.IntegerField()
    total_questions = models.IntegerField(default=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # NEW (Feature 3): Stores the user's streak value *at the time of this attempt*
    # Replacing the old 'streak_placeholder'
    current_streak = models.IntegerField(default=1)

    def __str__(self):
        user = self.device_id or "Anonymous"
        group = f" [{self.group_id}]" if self.group_id else ""
        return f"{user}{group} | Score: {self.score} | Streak: {self.current_streak}"


class LeaderboardEntry(models.Model):
    """
    Legacy model. 
    (Note: The MVP now uses real-time aggregation on QuizAttempt, 
    but we keep this model in case you want to cache top scores later).
    """
    name = models.CharField(max_length=100)
    high_score = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Leaderboard Entries"
    
    def __str__(self):
        return f"{self.name} - Score: {self.high_score}"

# --- NEW: Daily Reminder System ---

class DailyReminderSubscriber(models.Model):
    """
    Stores users who opted-in for daily email reminders.
    """
    email = models.EmailField(unique=True, help_text="User's email address for reminders.")
    created_at = models.DateTimeField(auto_now_add=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text="Uncheck to stop sending emails to this user.")
    
    # NEW: Persist the streak so we can recover it or display it in future emails
    current_streak = models.IntegerField(default=0)

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.email} ({status})"


# --- NEW: Group Viral Loop Models ---

class StudyGroup(models.Model):
    """
    Represents a class, youth group, or small group managed by a teacher.
    Generates a unique, short code for members to join.
    """
    name = models.CharField(max_length=100, help_text="e.g. 'Grace Youth - Wednesdays'")
    group_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # In a full auth system, you would link this to a User (Teacher)
    # teacher = models.ForeignKey(User, ...)

    def save(self, *args, **kwargs):
        # Auto-generate a unique 6-character code if not present
        if not self.group_code:
            self.group_code = get_random_string(length=6).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.group_code})"


class StudyGroupMember(models.Model):
    """
    Tracks anonymous users (device_id) who have 'joined' a group via invite link.
    """
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='members')
    device_id = models.CharField(max_length=255, db_index=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'device_id')

    def __str__(self):
        return f"{self.device_id} in {self.group.name}"


# --- NEW: Email Logging ---

class EmailLog(models.Model):
    """
    Simple log to track transactional emails and prevent duplicate sends.
    """
    EMAIL_TYPES = [
        ('welcome', 'Day 1: Welcome & PDF'),
        ('reminder', 'Daily Reminder'),
    ]
    
    subscriber = models.ForeignKey('DailyReminderSubscriber', on_delete=models.CASCADE, related_name='email_logs')
    email_type = models.CharField(max_length=50, choices=EMAIL_TYPES)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='sent')

    def __str__(self):
        return f"{self.email_type} -> {self.subscriber.email} ({self.sent_at.date()})"
