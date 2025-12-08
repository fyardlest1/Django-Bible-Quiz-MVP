import sys
import os
from django.core.management.base import BaseCommand
from quiz_api.models import Question, Category, LeaderboardEntry, CATEGORY_CHOICES

# Try importing the seeded data files. 
# We use try/except to warn you if the files haven't been generated or placed correctly.
try:
    # Assuming the file from the first step is named 'gtv_quiz_data.py' 
    # and contains the variable 'questions_to_seed'
    from bible_dataset.gtv_quiz_data import gtv_questions_to_seed as gtv_data
except ImportError:
    gtv_data = []
    print("Warning: Could not import 'gtv_quiz_data.py'. GTV questions will be empty.")

try:
    # Assuming the file from the second step is named 'ont_quiz_data.py'
    # and contains the variable 'ont_questions_to_seed'
    from bible_dataset.ont_quiz_data import ont_questions_to_seed as ont_data
except ImportError:
    ont_data = []
    print("Warning: Could not import 'ont_quiz_data.py'. ONT questions will be empty.")
    
try:
    # Assuming the file from the second step is named 'wst_quiz_data.py'
    # and contains the variable 'wst_questions_to_seed'
    from bible_dataset.wst_quiz_data import wst_questions_to_seed as wst_data
except ImportError:
    ont_data = []
    print("Warning: Could not import 'wst_quiz_data.py'. WST questions will be empty.")


class Command(BaseCommand):
    help = 'Seeds the database with initial categories and quiz questions from external files.'

    def handle(self, *args, **options):
        self.stdout.write("--- Seeding Initial Data ---")

        # ---------------------------------------------------------
        # 1. Seed Categories (Feature 2 Foundation)
        # ---------------------------------------------------------
        Category.objects.all().delete()
        for code, name in CATEGORY_CHOICES:
            Category.objects.create(name=name)
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(CATEGORY_CHOICES)} Categories.'))

        # ---------------------------------------------------------
        # 2. Seed Questions (Core Data)
        # ---------------------------------------------------------
        
        # Combine the lists imported from the external files
        all_questions_to_seed = gtv_data + ont_data + wst_data

        # If you have a manual list for 'Who Said This' (WST) you can add it here, 
        # otherwise we just rely on the imported files.
        # Example: all_questions_to_seed += wst_data 

        Question.objects.all().delete()
        
        count = 0
        for q_data in all_questions_to_seed:
            Question.objects.create(
                question_text=q_data['text'],
                choices=q_data['choices'],
                correct_answer=q_data['answer'],
                category=q_data['category'],
                explanation=q_data.get('explanation', '') # use .get() in case explanation is missing
            )
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Seeded {count} Questions.'))
        
        # ---------------------------------------------------------
        # 3. Seed Leaderboard Entries (Feature 5 Foundation)
        # ---------------------------------------------------------
        LeaderboardEntry.objects.all().delete()
        LeaderboardEntry.objects.create(name='Top Learner', high_score=100)
        LeaderboardEntry.objects.create(name='Scripture Guru', high_score=95)
        self.stdout.write(self.style.SUCCESS(f'Seeded Leaderboard Entries.'))
        

# to run:
# py manage.py seed_quiz_data_gtv_ont