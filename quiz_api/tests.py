from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from .models import Question, Category, QuizAttempt

'''
    How to Run the Tests

    To verify the application logic, run the following command in your terminal:
    
    python manage.py test quiz_api

    **Expected Output:**
    You should see output similar to this, indicating all 3 tests passed:
    ```text
    Creating test database for alias 'default'...
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.012s

    OK
    Destroying test database for alias 'default'...
'''

class BibleQuizTests(TestCase):
    def setUp(self):
        """
        Runs before EVERY test. Sets up a clean environment.
        """
        # 1. Clear cache to ensure tests don't interfere with each other
        cache.clear()
        self.client = APIClient()
        
        # 2. Setup Category
        self.category = Category.objects.create(name='Test Category')
        
        # 3. Create 10 dummy questions (enough to form a quiz of 7)
        self.questions = []
        for i in range(10):
            q = Question.objects.create(
                question_text=f'Question {i}',
                choices=['A', 'B', 'C', 'D'],
                correct_answer='A', # Always A for simplicity in testing
                category='GTV' 
            )
            self.questions.append(q)

    def test_daily_quiz_is_locked_by_cache(self):
        """
        CRITICAL: Verifies that the 'Daily Quiz' returns the EXACT same 
        set of questions for subsequent requests (The Daily Lock).
        """
        url = reverse('daily-quiz')
        
        # First call: Generates the quiz and caches it
        response_1 = self.client.get(url)
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_1.data), 7) # Should match QUIZ_SIZE
        
        # Extract IDs from first response
        first_quiz_ids = [q['id'] for q in response_1.data]

        # Second call: Should retrieve from cache, NOT generate new randoms
        response_2 = self.client.get(url)
        second_quiz_ids = [q['id'] for q in response_2.data]
        
        # Assert they are identical
        self.assertEqual(first_quiz_ids, second_quiz_ids)


    def test_submit_scoring_logic(self):
        """
        Verifies that the API correctly grades answers.
        """
        # Force generate a quiz to populate the cache (required for submission validation)
        quiz_url = reverse('daily-quiz')
        quiz_response = self.client.get(quiz_url)
        
        # Pick the first question from the generated quiz
        question_data = quiz_response.data[0]
        q_id = question_data['id']
        
        # We know from setUp that correct answer is 'A'
        
        submit_url = reverse('submit-answers')
        
        # 1. Test Correct Answer
        payload_correct = [
            {'question_id': q_id, 'selected_answer': 'A'}
        ]
        response = self.client.post(submit_url, payload_correct, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['score'], 1)
        self.assertTrue(response.data['results'][0]['is_correct'])

        # 2. Test Incorrect Answer
        payload_incorrect = [
            {'question_id': q_id, 'selected_answer': 'B'} # B is wrong
        ]
        response = self.client.post(submit_url, payload_incorrect, format='json')
        self.assertEqual(response.data['score'], 0)
        self.assertFalse(response.data['results'][0]['is_correct'])


    def test_real_leaderboard_aggregation(self):
        """
        Verifies that the Leaderboard sums up scores for the same device
        and ranks them correctly.
        """
        # Create attempts for User A (Total Score: 8)
        QuizAttempt.objects.create(device_id='user_A', score=5, total_questions=7)
        QuizAttempt.objects.create(device_id='user_A', score=3, total_questions=7)
        
        # Create attempts for User B (Total Score: 2)
        QuizAttempt.objects.create(device_id='user_B', score=2, total_questions=7)
        
        # Create attempt for User C (Total Score: 10) - Should be #1
        QuizAttempt.objects.create(device_id='user_C', score=10, total_questions=7)
        
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # The list should be ordered by score descending: C (10), A (8), B (2)
        
        # Check Rank 1 (User C) - Name masked as "User user_C..."
        self.assertIn('User user_C', response.data[0]['name']) 
        self.assertEqual(response.data[0]['high_score'], 10)
        
        # Check Rank 2 (User A)
        self.assertIn('User user_A', response.data[1]['name']) 
        self.assertEqual(response.data[1]['high_score'], 8)
        
        # Check Rank 3 (User B)
        self.assertIn('User user_B', response.data[2]['name']) 
        self.assertEqual(response.data[2]['high_score'], 2)



# How to Run the Tests
# Execute the following command in your terminal:
# python manage.py test quiz_api
