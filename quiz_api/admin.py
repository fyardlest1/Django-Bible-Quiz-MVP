from django.contrib import admin
from .models import Question, Category, QuizAttempt, LeaderboardEntry, DailyReminderSubscriber


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'category', 'correct_answer')
    list_filter = ('category',)
    search_fields = ('question_text', 'correct_answer')
    ordering = ('category', 'question_text')

    def question_text_short(self, obj):
        return obj.question_text[:75] + "..." if len(obj.question_text) > 75 else obj.question_text
    question_text_short.short_description = "Question"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    # UPGRADE: Added group_id and current_streak to the list view
    list_display = ('device_id', 'group_id', 'score', 'current_streak', 'timestamp')
    
    # UPGRADE: Add filtering by Group ID (useful for seeing specific church activity)
    list_filter = ('timestamp', 'group_id')
    
    search_fields = ('device_id', 'group_id')
    readonly_fields = ('timestamp',)


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'high_score', 'last_updated')
    ordering = ('-high_score',)

# --- NEW: Daily Reminder Subscriber Admin ---

@admin.register(DailyReminderSubscriber)
class DailyReminderSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at', 'last_sent_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email',)
    actions = ['activate_subscribers', 'deactivate_subscribers']

    @admin.action(description='Activate selected subscribers')
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Deactivate selected subscribers')
    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)

