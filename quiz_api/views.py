from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, pagination
from rest_framework.exceptions import NotFound
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta 
from django.db.models import Avg, Sum, Count
from django.core.cache import cache

from .models import Question, QuizAttempt, Category, LeaderboardEntry, CATEGORY_CHOICES
from .serializers import (
    QuestionSerializer, 
    AnswerSubmissionSerializer, 
    QuizAttemptSerializer,
    CategorySerializer, 
    LeaderboardEntrySerializer,
    UserStatsSerializer
)

# --- Pagination Configuration ---

class QuizPackPagination(pagination.PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 50

# --- Feature 1: Daily Random Quiz ---

class DailyQuizView(APIView):
    QUIZ_CACHE_KEY = "daily_quiz_questions"
    QUIZ_SIZE = 7 
    CACHE_TIMEOUT = 60 * 60 * 24 

    def get(self, request):
        questions_data = cache.get(self.QUIZ_CACHE_KEY)
        if questions_data is not None:
            return Response(questions_data)

        try:
            if Question.objects.count() < self.QUIZ_SIZE:
                 return Response({"error": "Not enough questions in database."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            random_questions = Question.objects.all().order_by('?')[:self.QUIZ_SIZE]
        except Exception:
            return Response({"error": "Error generating quiz."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        questions_data = QuestionSerializer(random_questions, many=True).data
        question_ids = [q['id'] for q in questions_data]
        cache.set(f"{self.QUIZ_CACHE_KEY}_ids", question_ids, self.CACHE_TIMEOUT)
        cache.set(self.QUIZ_CACHE_KEY, questions_data, self.CACHE_TIMEOUT)
        
        return Response(questions_data)

class SubmitQuizView(APIView):
    """
    POST: Submits answers.
    """
    def post(self, request):
        # 1. Capture tracking IDs
        device_id = request.query_params.get('device_id', None)
        
        # FIX: Safely check for group_id. 
        # Only try .get() if request.data is a dictionary. 
        # If it's a list (like in your tests), rely on query_params.
        group_id = request.query_params.get('group_id', None)
        if isinstance(request.data, dict):
            group_id = request.data.get('group_id') or group_id

        submission_serializer = AnswerSubmissionSerializer(data=request.data, many=True)
        submission_serializer.is_valid(raise_exception=True)
        validated_data = submission_serializer.validated_data
        
        submitted_q_ids = [item['question_id'] for item in validated_data]
        questions = Question.objects.filter(id__in=submitted_q_ids).in_bulk()
        
        score = 0
        results = []
        
        processed_submissions = [item for item in validated_data if item['question_id'] in questions]
        total_questions = len(processed_submissions)

        for submission in processed_submissions:
            q_id = submission['question_id']
            selected_answer = submission['selected_answer']
            question = questions.get(q_id)
            
            is_correct = False
            correct_answer = question.correct_answer
            explanation = question.explanation
            
            if str(selected_answer).strip().lower() == str(correct_answer).strip().lower():
                score += 1
                is_correct = True

            results.append({
                "question_id": q_id,
                "selected_answer": selected_answer,
                "is_correct": is_correct,
                "correct_answer": correct_answer,
                "explanation": explanation,
            })

        # --- STREAK ALGORITHM ---
        new_streak = 1 
        
        if device_id:
            last_attempt = QuizAttempt.objects.filter(device_id=device_id).order_by('-timestamp').first()
            
            if last_attempt:
                last_date = last_attempt.timestamp.date()
                today = timezone.now().date()
                yesterday = today - timedelta(days=1)
                
                if last_date == today:
                    new_streak = last_attempt.current_streak
                elif last_date == yesterday:
                    new_streak = last_attempt.current_streak + 1
                else:
                    new_streak = 1

        attempt = QuizAttempt.objects.create(
            score=score,
            total_questions=total_questions,
            device_id=device_id,
            group_id=group_id,
            current_streak=new_streak
        )
        attempt_data = QuizAttemptSerializer(attempt).data
        
        return Response({
            "score": score,
            "total_questions": total_questions,
            "streak": new_streak,
            "attempt_details": attempt_data,
            "results": results,
        })

# --- Feature 3: User Stats View ---

class UserStatsView(APIView):
    def get(self, request):
        device_id = request.query_params.get('device_id')
        
        if not device_id:
            return Response({"error": "device_id query parameter is required."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        attempts = QuizAttempt.objects.filter(device_id=device_id)
        
        if not attempts.exists():
            return Response({
                "total_quizzes": 0, "total_score": 0, "average_score": 0.0,
                "last_played": None, "current_streak": 0, "category_breakdown": {}
            })

        stats = attempts.aggregate(
            total_quizzes=Count('id'),
            total_score=Sum('score'),
            avg_score=Avg('score')
        )
        
        last_attempt = attempts.order_by('-timestamp').first()
        current_streak = 0
        
        if last_attempt:
            last_date = last_attempt.timestamp.date()
            today = timezone.now().date()
            if last_date >= today - timedelta(days=1):
                current_streak = last_attempt.current_streak
        
        category_breakdown = {
            "GTV": "N/A", 
            "WST": "N/A",
            "ONT": "N/A"
        }

        data = {
            "total_quizzes": stats['total_quizzes'],
            "total_score": stats['total_score'],
            "average_score": round(stats['avg_score'], 2),
            "last_played": last_attempt.timestamp if last_attempt else None,
            "current_streak": current_streak,
            "category_breakdown": category_breakdown
        }
        
        return Response(UserStatsSerializer(data).data)

# --- Feature 2: Category Packs ---

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class QuizPackQuestionsView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    pagination_class = QuizPackPagination

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        slug_map = { slugify(name): code for code, name in CATEGORY_CHOICES }
        category_code = slug_map.get(category_slug.lower())

        if not category_code:
            raise NotFound(f"Category '{category_slug}' not found.")
            
        return Question.objects.filter(category=category_code).order_by('?')

class RecentAttemptsView(generics.ListAPIView):
    queryset = QuizAttempt.objects.all().order_by('-timestamp')[:10]
    serializer_class = QuizAttemptSerializer

# --- Feature 5: Leaderboard ---

class LeaderboardView(APIView):
    def get(self, request):
        group_id = request.query_params.get('group_id')
        queryset = QuizAttempt.objects.all()
        
        if group_id:
            queryset = queryset.filter(group_id=group_id)

        leaderboard_data = queryset.values('device_id').annotate(
            total_score=Sum('score')
        ).order_by('-total_score')[:10]
        
        results = []
        for entry in leaderboard_data:
            d_id = entry['device_id']
            display_name = f"User {d_id[:6]}..." if d_id else "Anonymous"
            
            results.append({
                "name": display_name,
                "high_score": entry['total_score'],
                "last_updated": timezone.now() 
            })
            
        return Response(results)